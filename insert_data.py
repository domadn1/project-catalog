#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Category, Base, ProductItem

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


user1 = User(name="Thomas", email="thomas123@gmail.com", picture="https://indianapublicmedia.org/images/arts-images/profiles-harvey-g-cohen.jpg")
session.add(user1)
session.commit()
user2 = User(name="Mike", email="mike123@gmail.com", picture="https://a57.foxnews.com/static.foxnews.com/foxnews.com/content/uploads/2018/09/340/340/howard-kurtz.png?ve=1&tl=1")
session.add(user2)
session.commit()
user3 = User(name="Helan", email="helan123@gmail.com", picture="https://profilesofparis.com/wp-content/uploads/2018/05/Headshot-2017.jpg")
session.add(user3)
session.commit()
user4 = User(name="Jay", email="jay123@gmail.com", picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSITbitRJPTcFp2Lzo7X0d3eKetS54IcUbw7FKgYPxdHSpXC9go")
session.add(user4)
session.commit()
user5 = User(name="Neena", email="neena123@gmail.com", picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRLqcSrdNu2RABjUAlLIankn5rHkbTPsRHeJOFPiZqO2zSsvVD")
session.add(user5)
session.commit()

category1 = Category(name="Services")
session.add(category1)
session.commit()

category2 = Category(name="Electronics")
session.add(category2)
session.commit()

category3 = Category(name="Food Items")
session.add(category3)
session.commit()

category4 = Category(name="")
session.add(category4)
session.commit()

productItem1 = ProductItem(name="Apple In-Ear Headphones", description="Frequency: 5Hz to 21kHz, Impedance: 23 ohms, Sensitivity: 109 dB SPL/mW, Drivers: two-way balanced armature, Cable length: 1065 mm, Weight: 10.2 grams", price="$79", user=user1, category=category2)
session.add(productItem1)
session.commit()

productItem2 = ProductItem(name="Apple Wireless Keyboard", description="The sleek aluminium Apple Wireless Keyboard.", price="$47", user=user3, category=category2)
session.add(productItem2)
session.commit()

productItem3 = ProductItem(name="Bose Mini Bluetooth Speaker", description="Bose's smallest portable Bluetooth speaker", price="$279", user=user1, category=category2)
session.add(productItem3)
session.commit()

productItem4 = ProductItem(name="Alice's Adventures in Wonderland - Lewis Caroll", description="Alice's Adventures in Wonderland (commonly shortened to Alice in Wonderland) is an 1865 novel written by English author Charles Lutwidge Dodgson under the pseudonym Lewis Carroll. It tells of a girl named Alice falling through a rabbit hole into a fantasy world populated by peculiar, anthropomorphic creatures. The tale plays with logic, giving the story lasting popularity with adults as well as with children. It is considered to be one of the best examples of the literary nonsense genre. Its narrative course and structure, characters and imagery have been enormously influential in both popular culture and literature, especially in the fantasy genre.", price="$100", user=user1, category=category1)
session.add(productItem4)
session.commit()

productItem5 = ProductItem(name="Advanced CRM Functional", description="Learn directly from our team and network of Odoo experts. Choose from the available training sessions for a better functional understanding of Odoo", price="$999", user=user3, category=category1)
session.add(productItem5)
session.commit()

productItem6 = ProductItem(name="Functional Training", description="Learn directly from our team and network of Odoo experts. Choose from the available training sessions for a better functional understanding of Odoo", price="$900", user=user1, category=category1)
session.add(productItem6)
session.commit()

productItem7 = ProductItem(name="Ice Cream Chocolate", description="Ice Cream Chocolate with sticks", price="$10", user=user1, category=category3)
session.add(productItem7)
session.commit()

productItem8 = ProductItem(name="Technical Training", description="Learn directly from our team and network of Odoo experts. Choose from the available training sessions for a better technical understanding of Odoo", price="$500", user=user1, category=category1)
session.add(productItem8)
session.commit()

productItem9 = ProductItem(name="Speculoos", description="Speculaas or speculoos is a type of spiced shortcrust biscuit, traditionally baked for consumption on or just before St Nicholas' day in the Netherlands, Belgium, and around Christmas in Germany and Austria.", price="$25", user=user2, category=category3)
session.add(productItem9)
session.commit()

productItem10 = ProductItem(name="Milkshake Chocolate", description="This indulgent masterpiece is one seriously special treat. Serves chilled drink topped with marshmallows, cream and a drizzle of chocolate spread", price="$20", user=user2, category=category3)
session.add(productItem10)
session.commit()

productItem11 = ProductItem(name="Irish coffee", description="Irish coffee is a cocktail consisting of hot coffee, Irish whiskey, and sugar, stirred, and topped with cream. The coffee is drunk through the cream.", price="$10", user=user2, category=category3)
session.add(productItem11)
session.commit()

productItem12 = ProductItem(name='HP Pavilion Nontouch i7 17.3" HD Display Laptop', description='Loaded with a 7th Gen Core i7 Intel Processor, 8GB RAM, a storage capacity of 2TB Serial ATA Hard Drive, and a HD Intel Graphics 620 processor, the HP Pavilion offers great performance and room for multitasking. The keyboard comes with a numeric keypad to make your data entry super-fast and easy.', price="$2000", user=user1, category=category2)
session.add(productItem12)
session.commit()

productItem13 = ProductItem(name="Acer Aspire R 15 2-in-1 Laptop", description='Steel gray in color and featuring high level specs, including a 360o closing edge that provides you with four display modes, Acer Aspire R 15 is one of the best laptops that come with a numeric keypad to meet all typing needs fast and perfectly. It is packed with super-fast and powerful processing features including a latest 7th Gen Core i7 Intel processor with up to 3.5 GHz Turbo Boost Technology, 2GB NVIDIA GeForce 940MX processor, 12 GB system memory and 256GB SSD storage memory running on Windows 10 Operating System.', price="$2500", user=user1, category=category2)
session.add(productItem13)
session.commit()

productItem14 = ProductItem(name="Dell Inspiron 15 5000", description="One of the newest Dell models, Inspiron 15 5000 is a great laptop to own as it will allow you to do your work, including fast typing with ease with its 15.6 inch Full HD backlit keyboard that has a numeric keypad. It has a latest generation Intel 8th Quad Core processor with 6MB cache backed by up to 3.4GHz Turbo Boost Technology and a powerful Intel UHD Graphics 620. The RAM is 8GB and plenty of storage space with a 1TB HDD.", price="$1200", user=user3, category=category2)
session.add(productItem14)
session.commit()

productItem15 = ProductItem(name="HP 15.6 Touchscreen Laptop", description="The HP Touchscreen is another latest laptop model that marries design and powerful functionality. For the processor, memory and graphics, it features an Intel Core i5-7200U with up to 3.10 GHz Turbo Boost Technology, 8GB and Intel HD Graphics 620. It provides a lot of storage capacity with its 2TB HDD. For communication and connectivity, it is packed with a standard island-style keyboard featuring a numeric keypad, 802.11ac wireless LAN, digitally integrated microphone VGA webcam and modern Bluetooth technology.", price="$1999", user=user3, category=category2)
session.add(productItem15)
session.commit()

productItem16 = ProductItem(name="Lenovo Business Laptop", description="One of the most recent models from Lenovo, Lenovo Business Laptop is designed to offer high end computing capability including gaming, surfing net, watching movies, and more. It combines a smart Quad-Core Processor, and runs Windows 10 Operating system to enable fast processing performance. 12GB high- bandwidth RAM enable your tasks to run simultaneously and the 1TB HDD with a 5400 rpm spindle speed provides more than enough storage space and access for applications, files and documents.", price="$799", user=user1, category=category2)
session.add(productItem16)
session.commit()

productItem17 = ProductItem(name="ASUS TUF Thin, Light Gaming Laptop", description="Sporting a Red Matter Edition color theme, the ASUS TUF Gaming Laptop is equipped with a powerful NVIDIA GeForce GTX 1050 graphics coprocessor and a latest 8th-Gen Core i5 Intel processor, to enable faster multitasking performance for all your computing tasks including high-end gaming. It blends gaming performance and a durable life span due to its original Anti-Dust Cooling (ADC) system. It is also packed with high-frequency RAM and a FireCuda Hybrid SSD to ensure smooth sailing performance. In addition, it has a durable, unique and impressive red-backlit gaming keyboard featuring a numeric keypad to offer smooth and tactile keystrokes for quick data entry.", price="$2300", user=user3, category=category2)
session.add(productItem17)
session.commit()

productItem18 = ProductItem(name="LG Gram 15.6 Thin and Light Laptop", description="Weighing about 2.5 pounds, LG Gram Windows 10 Laptop has a cutting edge design architecture featuring a latest Gen i7 Intel processor, loads of RAM (16GB), Intel UHD Graphics 620 coprocessor, and high-speed 256 GB SSD storage capacity that combine together to facilitate a smooth high-end performance.", price="$2000", user=user1, category=category2)
session.add(productItem18)
session.commit()

productItem19 = ProductItem(name="Acer Aspire E15 Full HD Laptop", description="Backed by a powerful Intel Core i7 processor, lots of RAM memory and a contemporary graphics coprocessor, Acer Aspire E15 gives you the supremacy to work smoothly with both lightweight and heavy weight applications including games. Not only that, it is also packed with high-level modern features that give it a luxurious look including a comfortable keyboard embedded with a numeric keypad.", price="$2000", user=user1, category=category2)
session.add(productItem19)
session.commit()

productItem20 = ProductItem(name="Mojito", description="Mojito is a traditional Cuban highball. Traditionally, a mojito is a cocktail that consists of five ingredients: white rum, sugar, lime juice, soda water, and mint. Its combination of sweetness, citrus, and herbaceous mint flavors is intended to complement the rum, and has made the mojito a popular summer drink.", price="$12", user=user2, category=category3)
session.add(productItem20)
session.commit()

productItem21 = ProductItem(name="Pina Colada", description="The pina colada is a sweet cocktail made with rum, cream of coconut or coconut milk, and pineapple juice, usually served either blended or shaken with ice. It may be garnished with either a pineapple wedge, maraschino cherry, or both.", price="$30", user=user2, category=category3)
session.add(productItem21)
session.commit()

productItem22 = ProductItem(name="Margarita", description="A margarita is a cocktail consisting of tequila, orange liqueur, and lime juice often served with salt on the rim of the glass. The drink is served shaken with ice, blended with ice, or without ice.", price="$35", user=user2, category=category3)
session.add(productItem22)
session.commit()
