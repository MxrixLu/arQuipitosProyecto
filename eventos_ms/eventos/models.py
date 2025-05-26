import datetime

# Create your models here.

class Evento():

    id = str()
    nombre = str()
    hora = datetime.time()
    lugar = str()
    descripcion = str()
    tipo = str()

    paciente = str()
    doctor = str()

    def __str__(self):
        return self.nombre
    
    @staticmethod
    def from_mongo(dto):
        evento = Evento()
        evento.id = dto.get('_id', str())
        evento.nombre = dto.get('nombre', str())
        evento.hora = dto.get('hora', datetime.time())
        evento.lugar = dto.get('lugar', str())
        evento.descripcion = dto.get('descripcion', str())
        evento.paciente = dto.get('paciente', str())
        evento.doctor = dto.get('doctor', str())
        return evento

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

class Doctor():
    id = str()
    nombre = str()
    especialidad = str()
    telefono = str()
    email = str()

    def __str__(self):
        return self.nombre

    @staticmethod
    def from_mongo(dto):
        doctor = Doctor()
        doctor.id = dto.get('_id', str())
        doctor.nombre = dto.get('nombre', str())
        doctor.especialidad = dto.get('especialidad', str())
        doctor.telefono = dto.get('telefono', str())
        doctor.email = dto.get('email', str())
        return doctor