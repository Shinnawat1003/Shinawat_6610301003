import random
import time

# ฟังก์ชันสำหรับดึงข้อมูลจากไฟล์ SQL
def parse_sql_file():
    data = []
    with open('province.sql', 'r', encoding='utf-8') as file:
        for line in file:
            if "INSERT INTO" in line:
                parts = line.split("VALUES (")[1].split(")")[0].split(",")
                pcode = int(parts[0].strip())
                pname = parts[1].strip().strip("'")
                data.append((pcode, pname))
    return data

# ฟังก์ชันสุ่มข้อมูล
def randomize_data(dataset):
    randomized = dataset.copy()
    random.shuffle(randomized)
    return randomized

# Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][0] > arr[j+1][0]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key[0] < arr[j][0]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Selection Sort
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j][0] < arr[min_idx][0]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# Merge Sort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i][0] < R[j][0]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

# Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x[0] < pivot[0]]
    middle = [x for x in arr if x[0] == pivot[0]]
    right = [x for x in arr if x[0] > pivot[0]]
    return quick_sort(left) + middle + quick_sort(right)

# วัดเวลาการทำงาน
def measure_time(sort_function, dataset):
    start_time = time.time()
    sorted_data = sort_function(dataset.copy())
    end_time = time.time()
    return sorted_data, end_time - start_time

# ฟังก์ชันสำหรับบันทึกข้อมูลลงไฟล์ข้อความ
def save_to_txt(filename, sorted_data, durations):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("ID\tจังหวัด\n")
        for item in sorted_data:
            file.write(f"{item[0]}\t{item[1]}\n")
        file.write("\nผลการคำนวณของแต่ละอัลกอริทึม:\n")
        for algorithm, duration in durations.items():
            file.write(f"{algorithm}: {duration:.6f} วินาที\n")
    print(f"ข้อมูลถูกบันทึกลงไฟล์ {filename} เรียบร้อยแล้ว")

# ฟังก์ชันหลัก
def main():
    # อ่านข้อมูลจากไฟล์ SQL
    data = parse_sql_file()

    # สุ่มข้อมูลก่อนเรียงลำดับ
    randomized_data = randomize_data(data)
    print("ข้อมูลก่อนเรียงลำดับ:")
    for item in randomized_data:
        print(f"ID: {item[0]} จังหวัด: {item[1]}")

    # รายชื่ออัลกอริทึมการเรียงลำดับ
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
    }

    # ทดสอบแต่ละอัลกอริทึม
    durations = {}
    for name, func in algorithms.items():
        sorted_data, duration = measure_time(func, randomized_data)
        durations[name] = duration
        print(f"\n{name}:")
        for item in sorted_data:
            print(f"ID: {item[0]} จังหวัด: {item[1]}")
        print(f"เวลาที่ใช้: {duration:.6f} วินาที")

    # บันทึกข้อมูลที่เรียงลำดับและผลการคำนวณลงไฟล์ข้อความ
    save_to_txt('output_sorted_province.txt', sorted_data, durations)

if __name__ == "__main__":
    main()
