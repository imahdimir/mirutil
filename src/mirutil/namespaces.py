from dataclasses import dataclass


@dataclass
class MetadataColumns :
  startendcol: str = "Start End Column"
  start: str = "Start"
  end: str = "End"
  numrow: str = "Number of Rows"
  numcol: str = "Number of Columns"
  colnames: str = "Columns Names"