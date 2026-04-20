CATEGORIES = [
    "Electronics",
    "Computers",
    "Accessories",
    "Office Supplies",
    "Furniture",
    "Kitchen",
    "Home Appliances",
    "Gaming",
    "Fitness",
    "Outdoor",
    "Automotive",
    "Pet Supplies",
    "Books",
    "Toys",
    "Health"
]

WAREHOUSES = [
    ("North Distribution Center", "Monterrey"),
    ("South Distribution Center", "Puebla"),
    ("West Warehouse", "Guadalajara"),
    ("East Warehouse", "Merida"),
    ("Central Fulfillment Hub", "Mexico City")
]

SUPPLIER_PREFIXES = [
    "Global", "Prime", "Dynamic", "Nova", "Atlas",
    "Titan", "Blue", "Golden", "Elite", "NextGen",
    "Pioneer", "Vision", "Fusion", "Vertex", "Quantum"
]

SUPPLIER_SUFIXES = [
    "Supplies", "Trading", "Imports", "Distributors", "Solutions",
    "Industries", "Logistics", "Partners", "Wholesale", "Group"
]

PRODUCT_NAMES_BY_CATEGORY = {
    "Electronics": [
        "Bluetooth Speaker", "Smart Watch", "Wireless Earbuds", "Portable Charger",
        "USB Hub", "LED Monitor", "Power Bank", "Action Camera"
    ],
    "Computers": [
        "Laptop", "Gaming Mouse", "Mechanical Keyboard", "SSD Drive",
        "External Hard Drive", "Graphics Tablet", "CPU Cooler", "RAM Kit"
    ],
    "Accessories": [
        "Phone Case", "Backpack", "Desk Lamp", "Cable Organizer",
        "Laptop Stand", "Travel Adapter", "Screen Cleaner", "Stylus Pen"
    ],
    "Office Supplies": [
        "Notebook Pack", "Printer Paper", "Stapler", "Whiteboard Markers",
        "Desk Organizer", "Calculator", "Clipboard", "Paper Shredder"
    ],
    "Furniture": [
        "Office Chair", "Standing Desk", "Bookshelf", "Storage Cabinet",
        "Coffee Table", "Dining Chair", "TV Stand", "Folding Table"
    ],
    "Kitchen": [
        "Knife Set", "Cutting Board", "Blender", "Coffee Maker",
        "Rice Cooker", "Cookware Set", "Toaster", "Electric Kettle"
    ],
    "Home Appliances": [
        "Vacuum Cleaner", "Air Purifier", "Fan", "Portable Heater",
        "Dehumidifier", "Humidifier", "Iron", "Water Dispenser"
    ],
    "Gaming": [
        "Gaming Headset", "Controller", "Gaming Chair", "VR Headset",
        "Mouse Pad", "Console Stand", "Webcam", "Capture Card"
    ],
    "Fitness": [
        "Yoga Mat", "Dumbbell Set", "Resistance Bands", "Treadmill",
        "Foam Roller", "Exercise Bike", "Jump Rope", "Kettlebell"
    ],
    "Outdoor": [
        "Camping Tent", "Flashlight", "Cooler", "Sleeping Bag",
        "Hiking Backpack", "Portable Stove", "Lantern", "Water Bottle"
    ],
    "Automotive": [
        "Car Vacuum", "Tire Inflator", "Dash Camera", "Jump Starter",
        "Seat Cover", "Phone Mount", "Tool Kit", "Car Charger"
    ],
    "Pet Supplies": [
        "Pet Bed", "Dog Leash", "Cat Toy", "Food Bowl",
        "Pet Carrier", "Scratching Post", "Pet Shampoo", "Bird Cage"
    ],
    "Books": [
        "Programming Guide", "Cookbook", "Science Encyclopedia", "Novel Collection",
        "Children Story Book", "History Atlas", "Language Workbook", "Art Book"
    ],
    "Toys": [
        "Building Blocks", "Puzzle Set", "RC Car", "Board Game",
        "Doll House", "Action Figure", "Toy Train", "Educational Kit"
    ],
    "Health": [
        "First Aid Kit", "Thermometer", "Blood Pressure Monitor", "Massage Gun",
        "Vitamin Organizer", "Digital Scale", "Face Mask Pack", "Hand Sanitizer"
    ]
}

SAMPLE_USERS = [
    ("Warehouse Manager", "manager@inventory.com", "manager123", "admin"),
    ("Sales Operator", "sales@inventory.com", "sales123", "end_user"),
    ("Purchasing Agent", "purchasing@inventory.com", "purchase123", "end_user")
]


SUPPLIER_CATEGORY_PREFERENCES = {
    0: ["Electronics", "Computers", "Gaming"],
    1: ["Furniture", "Office Supplies", "Home Appliances"],
    2: ["Kitchen", "Home Appliances", "Furniture"],
    3: ["Fitness", "Health", "Outdoor"],
    4: ["Books", "Toys", "Office Supplies"],
    5: ["Automotive", "Outdoor", "Accessories"],
    6: ["Pet Supplies", "Health", "Home Appliances"],
    7: ["Electronics", "Accessories", "Gaming"],
    8: ["Computers", "Office Supplies", "Electronics"],
    9: ["Furniture", "Kitchen", "Home Appliances"]
}
