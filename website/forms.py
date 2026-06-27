from django import forms

from .models import Booking, ServiceOption


class BookingForm(forms.ModelForm):
    services = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=[],
    )

    class Meta:
        model = Booking
        fields = [
            "full_name",
            "email",
            "phone",
            "property_type",
            "services",
            "preferred_date",
            "preferred_time",
            "address",
            "message",
        ]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["services"].choices = [
            (opt.value, opt.label)
            for opt in ServiceOption.objects.filter(is_active=True)
        ]

    def clean_services(self):
        services = self.cleaned_data.get("services", [])
        if not services:
            raise forms.ValidationError("Please select at least one service.")
        return services
