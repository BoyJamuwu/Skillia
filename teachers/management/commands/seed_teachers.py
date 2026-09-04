"""Carga docentes de ejemplo.

Es idempotente: se identifica a cada docente por su nombre completo, así que
volver a correrlo actualiza los datos en vez de duplicar filas. Sirve tanto para
completar la ficha de los docentes que vinieron del campo `instructor` viejo
como para poblar la pantalla de Docentes con datos de prueba.

    python manage.py seed_teachers
    python manage.py seed_teachers --assign-courses
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from courses.models import Course
from teachers.models import Teacher

TEACHERS = [
    {
        "full_name": "Fernando Reveco",
        "headline": "Backend Developer en una fintech",
        "specialty": "Programacion",
        "years_experience": 11,
        "rating": 4.9,
        "email": "fernando.reveco@skillia.com",
        "linkedin_url": "https://www.linkedin.com/in/fernando-reveco-skillia",
        "photo_url": "https://i.pravatar.cc/400?img=12",
        "bio": (
            "Lleva más de una década construyendo APIs y sistemas de pagos que mueven "
            "millones de transacciones al mes. Empezó enseñando Python a sus compañeros "
            "de equipo y terminó armando la ruta de backend completa de Skillia.\n\n"
            "En sus cursos insiste en lo mismo: primero entender el problema, después "
            "elegir la herramienta."
        ),
    },
    {
        "full_name": "Camila Fuentes",
        "headline": "Product Designer, ex-agencia",
        "specialty": "Diseno",
        "years_experience": 8,
        "rating": 4.8,
        "email": "camila.fuentes@skillia.com",
        "linkedin_url": "https://www.linkedin.com/in/camila-fuentes-skillia",
        "photo_url": "https://i.pravatar.cc/400?img=45",
        "bio": (
            "Diseñó productos para startups de logística y salud antes de dedicarse a "
            "enseñar. Su obsesión son las interfaces que no necesitan explicación.\n\n"
            "Sus clases están llenas de rediseños en vivo: toma una pantalla real, la "
            "critica sin piedad y la vuelve a armar delante de la cámara."
        ),
    },
    {
        "full_name": "Andrés Villalobos",
        "headline": "Data Engineer en e-commerce",
        "specialty": "Datos",
        "years_experience": 9,
        "rating": 4.7,
        "email": "andres.villalobos@skillia.com",
        "linkedin_url": "https://www.linkedin.com/in/andres-villalobos-skillia",
        "photo_url": "https://i.pravatar.cc/400?img=33",
        "bio": (
            "Se dedica a que los datos lleguen limpios y a tiempo a quien tiene que "
            "tomar decisiones. Trabajó en pipelines que procesan el catálogo de varias "
            "tiendas grandes de la región.\n\n"
            "Enseña SQL y Python para datos partiendo siempre de un dataset sucio de "
            "verdad, no de uno de juguete."
        ),
    },
    {
        "full_name": "Valentina Soto",
        "headline": "Frontend Developer y docente",
        "specialty": "Programacion",
        "years_experience": 7,
        "rating": 4.9,
        "email": "valentina.soto@skillia.com",
        "linkedin_url": "https://www.linkedin.com/in/valentina-soto-skillia",
        "photo_url": "https://i.pravatar.cc/400?img=47",
        "bio": (
            "Especialista en React y accesibilidad web. Mantiene un par de librerías "
            "open source y da charlas sobre por qué el HTML semántico sigue importando.\n\n"
            "Sus alumnos terminan el curso con un portafolio desplegado, no con una "
            "carpeta de ejercicios sueltos."
        ),
    },
    {
        "full_name": "Matías Aguirre",
        "headline": "DevOps y arquitectura en la nube",
        "specialty": "Infraestructura",
        "years_experience": 12,
        "rating": 4.6,
        "email": "matias.aguirre@skillia.com",
        "linkedin_url": "https://www.linkedin.com/in/matias-aguirre-skillia",
        "photo_url": "https://i.pravatar.cc/400?img=68",
        "bio": (
            "Pasó de administrar servidores físicos a diseñar infraestructura como "
            "código. Le tocó migrar más de un monolito a contenedores sin apagar el "
            "negocio.\n\n"
            "Explica Docker, CI/CD y despliegues con la calma de quien ya rompió "
            "producción varias veces y sabe cómo se arregla."
        ),
    },
    {
        "full_name": "Josefa Miranda",
        "headline": "Growth y marketing digital",
        "specialty": "Marketing",
        "years_experience": 6,
        "rating": 4.8,
        "email": "josefa.miranda@skillia.com",
        "linkedin_url": "https://www.linkedin.com/in/josefa-miranda-skillia",
        "photo_url": "https://i.pravatar.cc/400?img=26",
        "bio": (
            "Armó desde cero el canal de adquisición de dos startups y sabe exactamente "
            "cuánto cuesta conseguir un cliente en cada una.\n\n"
            "Sus cursos son de números: cómo medir, qué métrica ignorar y cuándo cortar "
            "una campaña que no funciona."
        ),
    },
]


class Command(BaseCommand):
    help = "Crea o actualiza docentes de ejemplo."

    def add_arguments(self, parser):
        parser.add_argument(
            "--assign-courses",
            action="store_true",
            help="Asigna un docente a los cursos que hayan quedado sin uno.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for data in TEACHERS:
            full_name = data.pop("full_name")
            _, created = Teacher.objects.update_or_create(
                full_name=full_name, defaults=data
            )
            data["full_name"] = full_name  # el diccionario del módulo queda intacto
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  + {full_name}"))
            else:
                updated_count += 1
                self.stdout.write(f"  ~ {full_name} (actualizado)")

        self.stdout.write(
            self.style.SUCCESS(
                f"Docentes: {created_count} creados, {updated_count} actualizados."
            )
        )

        if options["assign_courses"]:
            self.assign_courses()

    def assign_courses(self):
        """Reparte los cursos huérfanos, prefiriendo un docente de la misma categoría."""
        orphans = Course.objects.filter(teacher__isnull=True)
        if not orphans.exists():
            self.stdout.write("Todos los cursos ya tienen docente asignado.")
            return

        teachers = list(Teacher.objects.all())
        if not teachers:
            self.stdout.write(self.style.WARNING("No hay docentes para asignar."))
            return

        for index, course in enumerate(orphans):
            match = next(
                (t for t in teachers if t.specialty.lower() == course.category.lower()),
                teachers[index % len(teachers)],
            )
            course.teacher = match
            course.save(update_fields=["teacher"])
            self.stdout.write(f"  {course.title} -> {match.full_name}")
