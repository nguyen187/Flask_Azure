// Lấy các phần tử cần thao tác
const homeLink = document.getElementById("home-link");
const dashboardLink = document.getElementById("dashboard-link");
const mlappLink = document.getElementById("mlapp-link");
const photoLink = document.getElementById("photo-link");

const homeSection = document.getElementById("home");
const dashboardSection = document.getElementById("dashboard");
const mlappSection = document.getElementById("mlapp");
const photoSection = document.getElementById("photo");


// Ẩn tất cả các phần nội dung trừ phần Home
dashboardSection.style.display = "none";
mlappSection.style.display = "none";
photoSection.style.display = "none";


// Thêm sự kiện click cho các link
homeLink.addEventListener("click", function(e) {
  e.preventDefault(); // Ngăn chặn trình duyệt đi đến URL trong href
  homeSection.style.display = "block";
  dashboardSection.style.display = "none";
  mlappSection.style.display = "none";
  photoSection.style.display = "none";

});

dashboardLink.addEventListener("click", function(e) {
  e.preventDefault(); // Ngăn chặn trình duyệt đi đến URL trong href
  homeSection.style.display = "none";
  dashboardSection.style.display = "block";
  mlappSection.style.display = "none";
  photoSection.style.display = "none";

});

mlappLink.addEventListener("click", function(e) {
  e.preventDefault(); // Ngăn chặn trình duyệt đi đến URL trong href
  homeSection.style.display = "none";
  dashboardSection.style.display = "none";
  mlappSection.style.display = "block";
  photoSection.style.display = "none";

});
photoLink.addEventListener("click", function(e) {
    e.preventDefault(); // Ngăn chặn trình duyệt đi đến URL trong href
    homeSection.style.display = "none";
    dashboardSection.style.display = "none";
    photoSection.style.display = "block";
    mlappSection.style.display = "none";
    
  
  });
// document.getElementById("home").innerHTML = "Hello, world!";
