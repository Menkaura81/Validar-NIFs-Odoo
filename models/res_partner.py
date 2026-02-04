from odoo import models, api, fields
import csv
import base64
import io
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nif_sin_validar = fields.Char(string='NIF sin validar')

    @api.model
    def validar_nif_desde_csv(self, datos_csv, nombre_columna='NIF'):
        resultados = []
        nombre_columna_min = nombre_columna.strip().lower()

        try:
            contenido_csv = base64.b64decode(datos_csv).decode('utf-8')
            lector_csv = csv.DictReader(io.StringIO(contenido_csv))

            for num_fila, fila in enumerate(lector_csv, start=2):
                nif = ''
                for clave, valor in fila.items():
                    if clave and clave.strip().lower() == nombre_columna_min:
                        nif = (valor or '').strip()
                        break

                if not nif:
                    resultados.append({
                        'fila': num_fila,
                        'nif': nif,
                        'valido': False,
                        'mensaje': 'NIF vacío'
                    })
                    continue

                nif_limpio = nif.upper().replace(' ', '')
                if nif_limpio.startswith('ES'):
                    nif_limpio = nif_limpio[2:]

                try:
                    es_valido = self._check_vat_number('ES', nif_limpio)
                    if es_valido:
                        resultados.append({
                            'fila': num_fila,
                            'nif': nif,
                            'valido': True,
                            'mensaje': 'NIF válido'
                        })
                    else:
                        resultados.append({
                            'fila': num_fila,
                            'nif': nif,
                            'valido': False,
                            'mensaje': 'NIF inválido'
                        })
                except Exception as e:
                    resultados.append({
                        'fila': num_fila,
                        'nif': nif,
                        'valido': False,
                        'mensaje': str(e)
                    })

        except Exception as e:
            _logger.error(f"Error al procesar CSV: {str(e)}")
            raise

        return resultados
