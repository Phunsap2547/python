import datetime

# ฟังก์ชันสำหรับรับข้อมูลลูกค้าจากผู้ใช้
def get_customer_data():
    customer_data = {
        'ชื่อ': input("กรุณากรอกชื่อ: "),
        'ที่อยู่': input("กรุณากรอกที่อยู่: "),
        'เบอร์โทร': input("กรุณากรอกเบอร์โทร: ")
    }
    return customer_data

# รายชื่อสินค้า
products = ['แตงโม', 'แอปเปิ้ล', 'ส้ม', 'กล้วย', 'ทุเรียน']

# ฟังก์ชันสำหรับแสดงรายการสินค้าและให้ผู้ใช้เลือก
def select_products():
    selected_products = {}
    print("\nรายการสินค้า:")
    for i, product in enumerate(products, 1):
        print(f"{i}. {product}")

    while True:
        choice = input("\nกรุณาเลือกสินค้าตามหมายเลข (หรือพิมพ์ 'สำเร็จ' เพื่อหยุดเลือก): ")
        if choice.lower() == 'สำเร็จ':
            break
        if choice.isdigit() and 1 <= int(choice) <= len(products):
            product = products[int(choice) - 1]
            quantity = int(input(f"กรุณากรอกจำนวนกล่องที่ต้องการสั่งซื้อสำหรับ {product}: "))
            selected_products[product] = quantity
        else:
            print("กรุณาเลือกหมายเลขที่ถูกต้อง")

    return selected_products

# ฟังก์ชันสำหรับบันทึกข้อมูลลงไฟล์
def save_data_to_txt(customer_data, selected_products, shortest_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"./order/customer_data_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as file:
        # บันทึกข้อมูลลูกค้า
        file.write("ข้อมูลลูกค้า:\n")
        for key, value in customer_data.items():
            file.write(f"{key}: {value}\n")

        # บันทึกสินค้าที่ผู้ใช้เลือกและจำนวนกล่อง
        file.write("\nสินค้าที่สั่งซื้อ:\n")
        for product, quantity in selected_products.items():
            file.write(f"{product}: {quantity} ลัง\n")

        # บันทึกพาธที่สั้นที่สุด
        file.write("\nพาธที่สั้นที่สุด:\n")
        if shortest_path:
            file.write(" -> ".join(shortest_path) + "\n")
        else:
            file.write("ไม่พบพาธ\n")
        
    print(f"\nข้อมูลถูกบันทึกในไฟล์: {filename}")

# คลาสสำหรับกราฟ
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, weight):
        if source not in self.graph:
            self.graph[source] = {}
        if destination not in self.graph:
            self.graph[destination] = {}
        self.graph[source][destination] = weight
        self.graph[destination][source] = weight  # Consider both directions

    def get_neighbors(self, node):
        return self.graph.get(node, {})

# ฟังก์ชันหาค่าพาธที่สั้นที่สุด
def find_shortest_path(graph, start, end):
    distances = {node: float('inf') for node in graph.graph} 
    previous = {node: None for node in graph.graph}
    distances[start] = 0
    queue = [start]

    while queue:
        current = min(queue, key=lambda node: distances[node])
        queue.remove(current)

        if current == end:
            return build_path(previous, end)

        for neighbor, weight in graph.get_neighbors(current).items():
            new_distance = distances[current] + weight
            if new_distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_distance
                previous[neighbor] = current
                if neighbor not in queue:
                    queue.append(neighbor)

    return None

# ฟังก์ชันสำหรับสร้างพาธ
def build_path(previous, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path

# ฟังก์ชันหลัก
def main():
    graph = Graph()

    # Adding routes to the map
    graph.add_edge("A", "B", 2)
    graph.add_edge("A", "C", 5)
    graph.add_edge("B", "C", 1)
    graph.add_edge("B", "D", 9)
    graph.add_edge("C", "E", 4)
    graph.add_edge("D", "E", 2)
    graph.add_edge("D", "F", 5)
    graph.add_edge("E", "F", 1)

    # รับข้อมูลลูกค้าและเลือกสินค้า
    customer_data = get_customer_data()
    selected_products = select_products()

    # รับข้อมูลจุดเริ่มต้นและจุดหมายปลายทาง
    start_location = input("จุดเริ่มต้น: ")
    end_location = input("จุดหมายปลายทาง: ")

    shortest_path = find_shortest_path(graph, start_location, end_location)

    # บันทึกข้อมูลลูกค้า สินค้า และพาธที่สั้นที่สุดลงในไฟล์
    save_data_to_txt(customer_data, selected_products, shortest_path)

    if shortest_path is not None:
        print("Shortest Path:", shortest_path)
    else:
        print("No path found.")

if __name__ == "__main__":
    main()
