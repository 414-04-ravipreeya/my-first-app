<div id="receipt">
    <h3>🧾 บิลใบเสร็จรับเงิน</h3>
    <div id="receipt-details"></div>
    <hr>
    <h4>ยอดรวมสุทธิ: <span id="receipt-total">0</span> บาท</h4>
    <p><i>ขอบคุณที่อุดหนุนค่ะ!</i></p>
</div>


const menuData = [
    { id: 1, name: 'Latte', price: 55 },
    { id: 2, name: 'Flat White', price: 60 },
    { id: 3, name: 'Popcorn Latte', price: 65 },
    { id: 4, name: 'Americano', price: 50 },
    { id: 5, name: 'Tiramisu', price: 85 },
    { id: 6, name: 'Banoffee Pie', price: 75 },
    { id: 7, name: 'Blueberry Cake', price: 80 }
];

let cart = {}; // เก็บรายการที่เลือก { id: quantity }

function updateCart(itemId, change) {
    cart[itemId] = (cart[itemId] || 0) + change;
    
    // ถ้าจำนวนลดลงจนเหลือ 0 หรือติดลบ ให้ลบออกจาก cart
    if (cart[itemId] <= 0) {
        delete cart[itemId];
    }
    
    renderMenu(); // อย่าลืมสร้างฟังก์ชัน renderMenu() และ renderReceipt()
    renderReceipt(); 
}

function calculateTotal() {
    let total = 0;
    menuData.forEach(item => {
        if (cart[item.id]) {
            total += cart[item.id] * item.price;
        }
    });
    return total; // คืนค่า total ออกไปใช้งาน
}

// ฟังก์ชันสำหรับอัปเดตหน้าใบเสร็จ
function renderReceipt() {
    const detailsContainer = document.getElementById('receipt-details');
    const totalContainer = document.getElementById('receipt-total');
    
    let detailsHTML = '';
    
    menuData.forEach(item => {
        if (cart[item.id]) {
            const itemTotal = cart[item.id] * item.price;
            detailsHTML += `<p>${item.name} x ${cart[item.id]} = ${itemTotal} บาท</p>`;
        }
    });
    
    detailsContainer.innerHTML = detailsHTML || '<p>ยังไม่มีรายการที่เลือก</p>';
    totalContainer.innerText = calculateTotal();
}

