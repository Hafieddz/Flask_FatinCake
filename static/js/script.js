// Loader 

window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");
  
    loader.classList.add("loader--hidden");
  
    loader.addEventListener("transitionend", () => {
      document.body.removeChild(loader);
    });
  });

// End Of Loader

// Navbar

const navbarEl = document.querySelector('.navbar');

window.addEventListener('scroll', () =>{
  if(window.scrollY >= 56 && window.innerWidth > 1000 ) {
    navbarEl.classList.add('navbar-scrolled')
  } else if (window.scrollY < 56) {
    navbarEl.classList.remove('navbar-scrolled')

  }

});


// End Of Navbar


// Cart Logic 

let btn_plus = document.querySelector('.increase-cart');
btn_plus.addEventListener('click', addCart);

let btn_minus = document.querySelector('.decrease-cart');
btn_minus.addEventListener('click', minCart);

let value = 1;

function addCart() {
	value++;
  document.querySelector('.cart-value span').textContent = value;
}

function minCart() {
  if(value > 1) {
    value--;
    document.querySelector('.cart-value span').textContent = value;
  } else {
    // Nothing happen
  }
}

// End of Cart

// User not login and pressing add to cart button 

$('#add-to-cart').click(function(){
  Swal.fire({
    title: "Belum Login",
    text: "Anda harus login terlebih dahulu!",
    icon: "error"
  });
})