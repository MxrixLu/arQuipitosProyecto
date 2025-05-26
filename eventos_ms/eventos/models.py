import datetime

# Create your models here.

class Evento():

    id = str()
    nombre = str()
    fecha = datetime.date.today()
    hora = datetime.time()
    lugar = str()
    descripcion = str()
    tipo = str()

    paciente_id = str()
    doctor_id = str()

    def __str__(self):
        return self.nombre
    
    @staticmethod
    def from_mongo(dto):
        evento = Evento()
        evento.id = dto.get('_id', str())
        evento.nombre = dto.get('nombre', str())
        fecha_str = dto.get('fecha')
        if fecha_str:
            try:
                # Try parsing with day first
                try:
                    evento.fecha = datetime.datetime.strptime(fecha_str, '%d/%m/%Y').date()
                except ValueError:
                    # If that fails, try parsing with year first
                    evento.fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                # If both formats fail, try with month first
                evento.fecha = datetime.datetime.strptime(fecha_str, '%m/%d/%Y').date()
        else:
            evento.fecha = None

        hora_str = dto.get('hora')
        if hora_str:
            try:
                # Try parsing with seconds first
                evento.hora = datetime.datetime.strptime(hora_str, '%H:%M:%S').time()
            except ValueError:
                # If that fails, try parsing without seconds
                evento.hora = datetime.datetime.strptime(hora_str, '%H:%M').time()
        else:
            evento.hora = None
        evento.lugar = dto.get('lugar', str())
        evento.descripcion = dto.get('descripcion', str())
        evento.paciente_id = dto.get('paciente_id', str())
        evento.doctor_id = dto.get('doctor_id', str())
        return evento
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'nombre': self.nombre,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'hora': self.hora.isoformat() if self.hora else None,
            'lugar': self.lugar,
            'descripcion': self.descripcion,
            'paciente_id': self.paciente_id,
            'doctor_id': self.doctor_id
        }

class Paciente():
    id = str()
    nombre = str()
    edad = int()
    sexo = str()
    direccion = str()
    telefono = str()
    email = str()

    def __str__(self):
        return self.nombre
    
    @staticmethod
    def from_mongo(dto):
        paciente = Paciente()
        paciente.id = dto.get('_id', str())
        paciente.nombre = dto.get('nombre', str())
        paciente.edad = dto.get('edad', int())
        paciente.sexo = dto.get('sexo', str())
        paciente.direccion = dto.get('direccion', str())
        paciente.telefono = dto.get('telefono', str())
        paciente.email = dto.get('email', str())
        return paciente
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'nombre': self.nombre,
            'edad': self.edad,
            'sexo': self.sexo,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email
        }

class Doctor():
    id = str()
    nombre = str()
    especialidad = str()
    telefono = str()
    email = str()

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            'id': str(self.id),
            'nombre': self.nombre,
            'especialidad': self.especialidad,
            'telefono': self.telefono,
            'email': self.email
        }

    @staticmethod
    def from_mongo(dto):
        doctor = Doctor()
        doctor.id = dto.get('_id', str())
        doctor.nombre = dto.get('nombre', str())
        doctor.especialidad = dto.get('especialidad', str())
        doctor.telefono = dto.get('telefono', str())
        doctor.email = dto.get('email', str())
        return doctor