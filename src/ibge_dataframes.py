from pathlib import Path
import pandas as pd

class AggregateTypes:
    DISTRITOS = "distritos"
    BAIRROS = "bairros"
    MUNICIPIOS = "municipios"
    SETORES = "setores"
    SUBDISTRITOS = "subdistritos"


class AggregatesBase(object):
    def __init__(self, path:Path, file_infix:str, folder_infix:str):
        self.path = path
        self.file_infix = file_infix
        self.folder_infix = folder_infix

    @staticmethod
    def __load_csv(path) -> pd.DataFrame:
        return pd.read_csv(path, encoding='Windows-1252', sep=';', low_memory=False)

    def _generate_path(self, filename: str) -> Path:
        folder = f"Agregados_por_{self.folder_infix}_csv"
        file = f"Agregados_por_{self.file_infix}_{filename}_BR.csv"
        return self.path / folder / file

    def load_literacy(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("alfabetizacao"))

    def load_basic(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("basico"))

    def load_household_characteristics1(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("caracteristicas_domicilio1"))

    def load_household_characteristics2(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("caracteristicas_domicilio2"))

    def load_household_characteristics3(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("caracteristicas_domicilio3"))

    def load_color_or_race(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("cor_ou_raca"))

    def load_demography(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("demografia"))

    def load_indigenous_households(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("domicilios_indigenas"))

    def load_quilombola_households(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("domicilios_quilombolas"))

    def load_deaths(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("obitos"))

    def load_kinship(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("parentesco"))

    def load_indigenous_people(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("pessoas_indigenas"))

    def load_quilombola_people(self) -> pd.DataFrame:
        return AggregatesBase.__load_csv(self._generate_path("pessoas_quilombolas"))

class AggregatesBairros(AggregatesBase):
    def __init__(self, path):
        super().__init__(path, AggregateTypes.BAIRROS, "Bairro")

class AggregatesDistritos(AggregatesBase):
    def __init__(self, path):
        super().__init__(path, AggregateTypes.DISTRITOS, "Distrito")

class AggregatesSubdistritos(AggregatesBase):
    def __init__(self, path):
        super().__init__(path, AggregateTypes.SUBDISTRITOS, "SubDistrito")

class AggregatesSetores(AggregatesBase):
    def __init__(self, path):
        super().__init__(path, AggregateTypes.SETORES, "Setor")

class AggregatesMunicipios(AggregatesBase):
    def __init__(self, path):
        super().__init__(path, AggregateTypes.MUNICIPIOS, "Municipio")

class AggregatesFactory:
    @staticmethod
    def get_aggregates(aggregate_type: str, path: Path) -> AggregatesBase:
        """
        Example usage
        from pathlib import Path

        path = Path("/path/to/files")

        aggregates = AggregatesFactory.get_aggregates(AggregateTypes.DISTRITOS, path)

        # Use autocompletion to explore available methods
        df_color = aggregates.load_color_or_race()
        df_demo = aggregates.load_demography()
        :param aggregate_type: The type of the aggregate.
        :param path: The base path where the census data is stored
        :return: The instance of the class
        """
        class_mapping = {
            AggregateTypes.DISTRITOS: AggregatesDistritos,
            AggregateTypes.BAIRROS: AggregatesBairros,
            AggregateTypes.MUNICIPIOS: AggregatesMunicipios,
            AggregateTypes.SETORES: AggregatesSetores,
            AggregateTypes.SUBDISTRITOS: AggregatesSubdistritos,
        }
        if aggregate_type not in class_mapping:
            raise ValueError(f"Invalid aggregate type: {aggregate_type}. Must be one of {list(class_mapping.keys())}.")
        return class_mapping[aggregate_type](path)