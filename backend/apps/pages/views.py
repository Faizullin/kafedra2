from django.views.generic import TemplateView

from lms.core.loading import get_model

Program = get_model("courses", "LMSProgram")
Course = get_model("courses", "LMSCourse")


class HomeView(TemplateView):
    template_name = "lms/pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programs = Program.objects.all()
        courses = Course.objects.all()
        countryZones = [
            {"title": "Russia", "coords": [37.8169909581523, 55.656739408787644], "IDENTIFIER_FIELD": "RUS"},
            {"title": "Ukraine", "coords": [30.470654500730177, 50.485578559550646], "IDENTIFIER_FIELD": "UKR"},
            {"title": "Slovakia", "coords": [18.36851273469742, 48.405070065084715], "IDENTIFIER_FIELD": "SVK"},
            {"title": "Hungary", "coords": [19.00052294372972, 47.49790641707506], "IDENTIFIER_FIELD": "HUN"},
            {"title": "Czechia", "coords": [14.443096686029122, 50.06473225156262], "IDENTIFIER_FIELD": "CZE"},
            {"title": "Kazakhstan", "coords": [71.57935000791193, 51.172554500320985], "IDENTIFIER_FIELD": "KAZ"},
        ]
        countryZonesPath = [
            {
                "from": "KAZ", "to": "RUS"},
            {
                "from": "RUS", "to": "UKR"},
            {
                "from": "UKR", "to": "SVK"},
            {
                "from": "SVK", "to": "CZE"},
            {
                "from": "SVK", "to": "HUN"},
        ]
        context.update({
            "countryZones": countryZones,
            "countryZonesPath": countryZonesPath,
            "programs": programs,
            "courses": courses,
        })
        print("data")
        return context
