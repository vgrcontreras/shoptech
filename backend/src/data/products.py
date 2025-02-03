import random

from faker import Faker

from backend.src.models import Product

fake = Faker()


brands_by_category = {
    'Mobile Devices': {
        'Smartphones': ['Apple', 'Samsung', 'Google', 'OnePlus'],
        'Tablets': ['Apple', 'Samsung', 'Lenovo', 'Microsoft'],
    },
    'Computers and Accessories': {
        'Laptops': ['Dell', 'HP', 'Apple', 'Lenovo'],
        'Desktops': ['Dell', 'HP', 'Lenovo', 'Acer'],
        'Monitors': ['LG', 'Samsung', 'Dell', 'Acer'],
        'Keyboards': ['Logitech', 'Razer', 'Corsair', 'Microsoft'],
        'Mice': ['Logitech', 'Razer', 'SteelSeries', 'Corsair'],
        'External Hard Drives': [
            'Western Digital',
            'Seagate',
            'Toshiba',
            'LaCie',
        ],
    },
    'Audio and Wearables': {
        'Headphones': ['Sony', 'Bose', 'Sennheiser', 'Audio-Technica'],
        'Earbuds': ['Apple', 'Samsung', 'Sony', 'Jabra'],
        'Bluetooth Speakers': ['JBL', 'Sony', 'Bose', 'Ultimate Ears'],
        'Smartwatches': ['Apple', 'Samsung', 'Fitbit', 'Garmin'],
    },
    'Cameras and Accessories': {
        'DSLR Cameras': ['Canon', 'Nikon', 'Sony', 'Pentax'],
        'Action Cameras': ['GoPro', 'DJI', 'Sony', 'Insta360'],
        'Camera Lenses': ['Canon', 'Nikon', 'Tamron', 'Sigma'],
        'Drones': ['DJI', 'Parrot', 'Autel Robotics', 'Skydio'],
    },
    'Gaming': {
        'Gaming Consoles': [
            'Sony (PlayStation)',
            'Microsoft (Xbox)',
            'Nintendo',
            'Valve (Steam Deck)',
        ],
        'Gaming Laptops': ['Alienware', 'ASUS ROG', 'MSI', 'Acer Predator'],
        'VR Gaming Devices': [
            'Meta (Oculus)',
            'Sony (PS VR)',
            'HTC Vive',
            'Valve Index',
        ],
    },
    'Smart Home Devices': {
        'Smart Speakers': [
            'Amazon (Echo)',
            'Google (Nest)',
            'Apple (HomePod)',
            'Sonos',
        ],
        'Smart Plugs': ['TP-Link', 'Belkin', 'Wemo', 'Amazon'],
        'Smart Lights': ['Philips Hue', 'LIFX', 'Nanoleaf', 'Yeelight'],
        'Robot Vacuums': ['iRobot (Roomba)', 'Ecovacs', 'Roborock', 'Shark'],
    },
}


def generate_products_data():
    category = fake.random_element((brands_by_category.keys()))
    sub_category = fake.random_element((brands_by_category[category].keys()))
    brand = fake.random_element(brands_by_category[category][sub_category])

    products = Product(
        name=fake.word().capitalize() + ' ' + sub_category,
        category=category,
        sub_category=sub_category,
        brand=brand,
        price=round(random.uniform(50.0, 1000.0), 2),
    )

    return products
