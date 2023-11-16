
// Loader 

window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");
  
    loader.classList.add("loader--hidden");
  
    loader.addEventListener("transitionend", () => {
      document.body.removeChild(loader);
    });
  });

// End Of Loader


// Cart Logic 

let btn_plus = document.querySelector('.increase-cart');
btn_plus.addEventListener('click', addCart);

let btn_minus = document.querySelector('.decrease-cart');
btn_minus.addEventListener('click', minCart);

// variable outside all functions, retains value until page is reloaded / left
let value = 0;

function addCart() {
	value++;
  document.querySelector('.cart-value span').textContent = value;
}

function minCart() {
  if(value > 0) {
    value--;
    document.querySelector('.cart-value span').textContent = value
  } else {
    // Nothing happen
  }
}

// End of Cart
  
  