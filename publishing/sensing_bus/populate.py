import os

#def populate():
    print "Populating..."

def add_bus(name):
    p = Page.objects.get_or_create(name=name)[0]
    return p

def add_stop(lat, lng):
    c = Category.objects.get_or_create(lat=lat, lng=lng)[0]
    return c
    
def add_measurement(bus, stop, time, temperature, humidity, light, rain):
    c = Category.objects.get_or_create(bus=bus,stop=stop, time=time, 
                                       temperature=temperature, humidity=humidity,
                                       light=light, rain=rain)[0]
    return c
    
# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensing_bus.settings')
    from publisher.models import Bus,, Stop, Measurement
    populate()
