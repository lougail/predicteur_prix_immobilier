import pandas as pd
import os
from typing import Dict, Optional
from pathlib import Path

class DVFDataProcessor:
    """Classe pour traiter les données DVF (Demandes de Valeurs Foncières)."""

    SURFACE_REELLE_BATI_COL = 'Surface reelle bati'
    VALEUR_FONCIERE_COL = 'Valeur fonciere'
    
    def __init__(self, input_file: str, output_dir: str = "data"):
        """
        Initialise le processeur de données DVF.
        
        Args:
            input_file (str): Chemin vers le fichier de données DVF
            output_dir (str): Dossier de destination pour les fichiers traités
        """
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.data: Optional[pd.DataFrame] = None
        
    def load_data(self) -> None:
        """Charge les données DVF et effectue le prétraitement initial."""
        self.data = pd.read_csv(self.input_file, sep='|', low_memory=False)
        self.data['Commune'] = self.data['Commune'].str.upper()
    
    def filter_city_data(self, city: str) -> pd.DataFrame:
        """
        Filtre et traite les données pour une ville spécifique.
        
        Args:
            city (str): Nom de la ville en majuscules
            
        Returns:
            pd.DataFrame: Données filtrées et traitées pour la ville
        """
        if self.data is None:
            raise ValueError("Les données n'ont pas été chargées. Appelez load_data() d'abord.")
        df_city = self.data[
            (self.data['Commune'] == city) &
            (self.data['Nature mutation'] == 'Vente') &
            (self.data[self.SURFACE_REELLE_BATI_COL].notna()) &
            (self.data[self.VALEUR_FONCIERE_COL].notna())
        ].copy()
        
        return self._process_city_data(df_city)
    
    def _process_city_data(self, df_city: pd.DataFrame) -> pd.DataFrame:
        """
        Traite les données d'une ville (méthode privée).
        
        Args:
            df_city (pd.DataFrame): DataFrame de la ville à traiter
            
        Returns:
            pd.DataFrame: DataFrame traité
        """
        for col in ['Valeur fonciere', self.SURFACE_REELLE_BATI_COL]:
            df_city[col] = (df_city[col].astype(str)
                           .str.replace(',', '.')
                           .str.replace(' ', '')
                           .astype(float))
        # Calcul du prix au m²
        df_city['prix_m2'] = df_city[self.VALEUR_FONCIERE_COL] / df_city[self.SURFACE_REELLE_BATI_COL]
        
        return df_city
    
    def process_and_save_all(self) -> None:
        """Traite et sauvegarde les données pour toutes les villes configurées."""
        if self.data is None:
            self.load_data()
            
        # Création du dossier de sortie
        self.output_dir.mkdir(exist_ok=True)
        
        # Configuration des villes
        cities: Dict[str, str] = {
            'LILLE': 'lille_2022.csv',
            'BORDEAUX': 'bordeaux_2022.csv'
        }
        
        # Traitement pour chaque ville
        for city, output_file in cities.items():
            df_city = self.filter_city_data(city)
            output_path = self.output_dir / output_file
            df_city.to_csv(output_path, index=False)
            print(f"Fichier exporté : {output_path}")

def main():
    """Point d'entrée principal pour le traitement des données."""
    processor = DVFDataProcessor("data/ValeursFoncieres-2022.txt")
    processor.process_and_save_all()
    print("Traitement terminé.")

if __name__ == "__main__":
    main()