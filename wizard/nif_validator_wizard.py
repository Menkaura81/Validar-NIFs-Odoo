from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import csv
import io


class AsistenteValidadorNif(models.TransientModel):
    _name = 'nif.validator.wizard'
    _description = 'Validador de NIF desde CSV'

    archivo_csv = fields.Binary(
        string='Archivo CSV',
        required=True,
        help='Archivo CSV que desea comprobar'
    )
    nombre_archivo_csv = fields.Char(string='Nombre del archivo')
    nombre_columna = fields.Char(
        string='Nombre columna a validar',
        required=True,
        default='NIF',
        help='Nombre de la columna del CSV que contiene los NIFs a validar'
    )
    ids_resultado = fields.One2many(
        'nif.validator.result',
        'id_asistente',
        string='Resultados'
    )
    procesado = fields.Boolean(default=False)

    archivo_resultado = fields.Binary(string='Archivo Resultado', readonly=True)
    nombre_archivo_resultado = fields.Char(string='Nombre archivo resultado')

    def accion_validar(self):
        self.ensure_one()

        if not self.archivo_csv:
            raise UserError(_('Debe seleccionar un archivo CSV'))

        if self.nombre_archivo_csv and not self.nombre_archivo_csv.lower().endswith('.csv'):
            raise UserError(_('El archivo debe ser de tipo CSV'))

        if not self.nombre_columna:
            raise UserError(_('Debe especificar el nombre de la columna a validar'))

        nombre_col = self.nombre_columna.strip()

        contenido_csv = base64.b64decode(self.archivo_csv).decode('utf-8')
        lector_csv = csv.DictReader(io.StringIO(contenido_csv))

        campos_originales = lector_csv.fieldnames or []
        campos_nuevos = list(campos_originales) + ['NIF_validos']

        resultados = self.env['res.partner'].validar_nif_desde_csv(
            datos_csv=self.archivo_csv,
            nombre_columna=nombre_col
        )

        validacion_por_fila = {res['fila']: res for res in resultados}

        salida = io.StringIO()
        escritor = csv.DictWriter(salida, fieldnames=campos_nuevos)
        escritor.writeheader()

        contenido_csv = base64.b64decode(self.archivo_csv).decode('utf-8')
        lector_csv = csv.DictReader(io.StringIO(contenido_csv))

        for num_fila, fila in enumerate(lector_csv, start=2):
            valor_nif = ''
            for clave, valor in fila.items():
                if clave and clave.strip().lower() == nombre_col.lower():
                    valor_nif = (valor or '').strip()
                    break

            validacion = validacion_por_fila.get(num_fila, {})
            if validacion.get('valido'):
                fila['NIF_validos'] = valor_nif
            else:
                fila['NIF_validos'] = ''

            escritor.writerow(fila)

        csv_resultado = salida.getvalue()
        self.archivo_resultado = base64.b64encode(csv_resultado.encode('utf-8'))
        self.nombre_archivo_resultado = 'resultado_validacion_nif.csv'

        self.ids_resultado.unlink()

        valores_resultado = []
        for res in resultados:
            valores_resultado.append({
                'id_asistente': self.id,
                'numero_fila': res['fila'],
                'nif': res['nif'],
                'es_valido': res['valido'],
                'mensaje': res['mensaje'],
            })

        self.env['nif.validator.result'].create(valores_resultado)
        self.procesado = True

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'nif.validator.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }


class ResultadoValidadorNif(models.TransientModel):
    _name = 'nif.validator.result'
    _description = 'Resultado de validación de NIF'

    id_asistente = fields.Many2one('nif.validator.wizard', string='Asistente', ondelete='cascade')
    numero_fila = fields.Integer(string='Fila')
    nif = fields.Char(string='NIF')
    es_valido = fields.Boolean(string='Válido')
    mensaje = fields.Char(string='Mensaje')
