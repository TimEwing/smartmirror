
from django.template import Engine, Context
from django.conf import settings
from datetime import datetime, timedelta

import weather

def run():
    pass

def setup(display_template='display.html'):
    # Template shit
    # Django settings
    try:
        settings.configure()
    except RuntimeError:
        pass
    # Django template rendering engine
    engine = Engine(dirs=['.'])
    # Django template
    template = engine.get_template(display_template)
    # Django context (can be treated like normal dict)
    context = Context({'ass' : 'nope'})


    # Weather shit
    owm = weather.owm
    return template, context, owm

def display():
    pass

def test():
    template, context, owm = setup("test.html")
    fc = owm.three_hours_forecast("Boulder,CD,USA")

    wids = []
    times = []
    descs = []
    for hour_offset in range(48):
        tomorrow = datetime.now() + timedelta(days=1)
        dt = tomorrow + timedelta(hours=hour_offset)
        w = fc.get_weather_at(dt)
        wids.append(w.get_weather_code())
        print(w.get_weather_code())
        times.append(hour_offset % 12 + 1)
        descs.append(w.get_detailed_status() + " " + str(dt))

    context['wids'] = wids
    context['times'] = times
    context['descs'] = descs

    with open("tmp.html", "w") as tmp_out:
        tmp_out.write(template.render(context))

if __name__ == '__main__':
    print(setup())
