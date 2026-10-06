from django import forms

from courses.models import Course, Lesson, Module

INPUT_CLASSES = (
    "w-full bg-gray-100 rounded-lg py-3 px-3 border-2 border-transparent "
    "focus:border-primary focus:outline-none"
)


class PanelFormMixin:
    """Le da a todos los campos el mismo estilo que los formularios de registro."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLASSES)


class CourseForm(PanelFormMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = ("title", "description", "category", "duration", "price", "image_url")
        labels = {
            "title": "Título",
            "description": "Descripción",
            "category": "Categoría",
            "duration": "Duración",
            "price": "Precio (CLP)",
            "image_url": "URL de la imagen de portada",
        }
        help_texts = {"duration": 'Texto libre, por ejemplo "12 horas".'}
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}


class ModuleForm(PanelFormMixin, forms.ModelForm):
    class Meta:
        model = Module
        fields = ("title", "order")
        labels = {"title": "Título del módulo", "order": "Orden"}
        help_texts = {"order": "Los módulos se muestran de menor a mayor."}


class LessonForm(PanelFormMixin, forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("title", "duration", "video_url", "order")
        labels = {
            "title": "Título de la lección",
            "duration": "Duración",
            "video_url": "URL del video",
            "order": "Orden",
        }
        help_texts = {
            "duration": 'Por ejemplo "12:30".',
            "video_url": "Enlace directo al archivo (.mp4). Si se deja vacío se usa un video de muestra.",
            "order": "Las lecciones se muestran de menor a mayor dentro del módulo.",
        }
