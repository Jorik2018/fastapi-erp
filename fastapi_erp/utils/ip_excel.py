from datetime import datetime, timezone
from io import BytesIO
from typing import Iterable

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from fastapi_erp.model.base.ip import UtiIp


# Nombre del encabezado, atributo del modelo y ancho de columna.
IP_COLUMNS = [
    ("ID", "id", 10),
    ("CATEGORIA", "category", 25),
    ("CODIGO", "code", 20),
    ("NOMBRE", "name", 30),
    ("CARGO", "position", 25),
    ("ANTIVIRUS", "antivirus", 25),
    ("DESCRIPCION", "description", 30),
    ("RESTRICCION", "restriction", 25),
    ("MACID", "mac_id", 25),
    ("GRUPO TRABAJO", "workgroup", 25),
    ("EQUIPO", "device", 25),
    ("CODIGO PATRIMONIAL", "patrimonial_code", 25),
    ("USUARIO", "user", 20),
    ("FECHA CREACION", "creation", 22),
    ("FECHA ACTUALIZACION", "updated", 22),
    ("ESTABILIZADOR CODIGO PATRIMONIAL", "stabilizer_code", 30),
    ("ESTABILIZADOR DESCRIPCION", "stabilizer_description", 30),
    ("IMPRESORA CODIGO PATRIMONIAL", "printer_code", 30),
    ("IMPRESORA MODELO", "printer_model", 25),
    ("IMPRESORA SERIE", "printer_serie", 25),
    ("IMPRESORA DESCRIPCION", "printer_description", 30),
]


def generate_ip_excel(items: Iterable[UtiIp]) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "IPs"

    # Crear encabezados y configurar anchos.
    for index, (title, _, width) in enumerate(IP_COLUMNS, start=1):
        cell = sheet.cell(row=1, column=index, value=title)
        cell.font = Font(bold=True)

        letter = get_column_letter(index)
        sheet.column_dimensions[letter].width = width

    sheet.freeze_panes = "A2"

    # Agregar los registros.
    for row_index, item in enumerate(items, start=2):
        for col_index, (_, attribute, _) in enumerate(IP_COLUMNS, start=1):
            value = getattr(item, attribute)

            # Excel no admite fechas con zona horaria.
            if isinstance(value, datetime) and value.utcoffset() is not None:
                value = value.astimezone(timezone.utc).replace(tzinfo=None)

            cell = sheet.cell(
                row=row_index,
                column=col_index,
                value=value,
            )

            if isinstance(value, datetime):
                cell.number_format = "dd/mm/yyyy hh:mm:ss"

            # Evitar que una cadena que comienza con "=" sea una fórmula.
            if isinstance(value, str):
                cell.data_type = "s"

    output = BytesIO()
    workbook.save(output)

    return output.getvalue()
