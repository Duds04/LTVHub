from src.workflows.task import Task
import pandas as pd
from pathlib import Path

class CsvReadTask(Task):
    def __init__(
        self,
        name: str,
        fp: str,
        columnID: str = "id",
        columnDate: str = "date",
        columnMonetary: str = "monetary",
    ) -> None:
        super().__init__(name)
        self.fp = Path(fp)
        self.columnID = columnID
        self.columnDate = columnDate
        self.columnMonetary = columnMonetary

    def on_run(self) -> pd.DataFrame:
        df = pd.read_csv(self.fp)
        df.rename(
            columns={self.columnID: "id",
                     self.columnDate: "date", self.columnMonetary: "monetary"},
            inplace=True,
        )

        assert "id" in df.columns, f"ID column 'id' not found in DataFrame columns: {df.columns}"
        assert "date" in df.columns, f"Date column 'dt' not found in DataFrame columns: {df.columns}"
        assert "monetary" in df.columns, f"Monetary column 'monetary' not found in DataFrame columns: {df.columns}"

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            
        return df
