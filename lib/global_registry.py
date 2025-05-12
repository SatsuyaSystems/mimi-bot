import logging
from typing import Any, Callable, Dict, Optional

class GlobalRegistry:
    """
    Eine einfache Registry zur Verwaltung global geteilter Singleton-Instanzen.
    Verwendet einen eindeutigen Schlüssel, um Instanzen zu speichern und abzurufen.
    Stellt sicher, dass für jeden Schlüssel nur eine Instanz erstellt wird.
    """
    _instance = None # Für das Singleton-Pattern der Registry selbst

    def __new__(cls, *args, **kwargs):
        # Stellt sicher, dass nur eine Instanz der Registry selbst existiert
        if cls._instance is None:
            cls._instance = super(GlobalRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self._registry: Dict[str, Any] = {}
        self._initialized = True
        logging.info("GlobalRegistry initialized.")

    def get_or_create(self, key: str, instance_factory: Callable[[], Any], *factory_args, **factory_kwargs) -> Any:
        """
        Ruft eine Instanz anhand ihres Schlüssels ab oder erstellt sie, falls sie nicht existiert.

        Args:
            key (str): Der eindeutige Schlüssel für die Instanz (z.B. "databases.memory", "models.embedding").
                       Punktnotation hier ist nur ein Namenskonvention, intern wird es als flacher Key behandelt.
            instance_factory (Callable[[], Any]): Eine Funktion oder ein Klassenkonstruktor,
                                                  der aufgerufen wird, um die Instanz zu erstellen,
                                                  *nur* wenn der Schlüssel noch nicht existiert.
            *factory_args: Positionsargumente, die an instance_factory übergeben werden.
            **factory_kwargs: Schlüsselwortargumente, die an instance_factory übergeben werden.


        Returns:
            Any: Die existierende oder neu erstellte Instanz.
        """
        if key not in self._registry:
            logging.info(f"Creating new instance for key '{key}'...")
            try:
                # Erstelle die Instanz nur, wenn sie nicht im Registry ist
                self._registry[key] = instance_factory(*factory_args, **factory_kwargs)
                logging.info(f"Instance created and registered for key '{key}'.")
            except Exception as e:
                 logging.error(f"Failed to create instance for key '{key}': {e}", exc_info=True)
                 # Fehler weitergeben, damit die Anwendung merkt, dass etwas schiefgelaufen ist
                 raise
        else:
            logging.debug(f"Returning existing instance for key '{key}'.")

        return self._registry[key]

    def get(self, key: str) -> Optional[Any]:
        """
        Ruft eine Instanz anhand ihres Schlüssels ab, ohne sie zu erstellen.

        Args:
            key (str): Der Schlüssel der abzurufenden Instanz.

        Returns:
            Optional[Any]: Die Instanz, wenn sie existiert, sonst None.
        """
        return self._registry.get(key)

    def exists(self, key: str) -> bool:
        """Prüft, ob ein Schlüssel in der Registry existiert."""
        return key in self._registry

    def clear_key(self, key: str):
        """Entfernt einen Schlüssel und die zugehörige Instanz aus der Registry."""
        if key in self._registry:
            logging.info(f"Removing instance for key '{key}' from registry.")
            # Optional: Prüfen, ob die Instanz eine close() Methode hat und diese aufrufen
            instance = self._registry[key]
            if hasattr(instance, 'close') and callable(getattr(instance, 'close')):
                try:
                    logging.debug(f"Calling close() method for instance with key '{key}'.")
                    instance.close()
                except Exception as e:
                    logging.warning(f"Error calling close() for instance '{key}': {e}", exc_info=True)
            del self._registry[key]
        else:
             logging.debug(f"Key '{key}' not found in registry for clearing.")

    def clear_all(self):
        """Leert die gesamte Registry und ruft ggf. close() auf."""
        logging.warning("Clearing all instances from GlobalRegistry.")
        keys_to_clear = list(self._registry.keys()) # Kopie der Schlüssel, da wir das Dict ändern
        for key in keys_to_clear:
            self.clear_key(key)
        logging.info("GlobalRegistry cleared.")

g_data = GlobalRegistry()