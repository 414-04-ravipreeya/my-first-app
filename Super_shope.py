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
            if (cart[itemId] < 0) cart[itemId] = 0;
            renderMenu();
}

function calculateTotal() {
            let total = 0;
            menuData.forEach(item => {
                if (cart[item.id]) {
                    total += cart[item.id] * item.price;
                }
            });
          
