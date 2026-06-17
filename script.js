/* Fade-in / Fade-out Observer — chạy ngay lập tức vì script được load sau khi DOM đã sẵn sàng */
(function () {
  const sections = document.querySelectorAll(
    '.hero-section, .profile-section, .event-section, .video-section, .partners-section, .footer-section'
  );

  if (!sections.length) {
    console.warn('No sections found for fade effect.');
    return;
  }

  // Gắn class ẩn ban đầu
  sections.forEach(section => section.classList.add('fade-section'));

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
      } else {
        entry.target.classList.remove('is-visible');
      }
    });
  }, {
    threshold: 0.1
  });

  sections.forEach(section => observer.observe(section));

  console.log(`Fade observer attached to ${sections.length} sections.`);

  // --- Hiệu ứng đếm số (Count-up Animation) ---
  const counters = document.querySelectorAll('.count-up');
  
  if (counters.length > 0) {
    const animateCounter = (counter) => {
      const target = +counter.getAttribute('data-target');
      const prefix = counter.getAttribute('data-prefix') || '';
      const suffix = counter.getAttribute('data-suffix') || '';
      const duration = 2000; // 2 seconds animation
      
      let current = 0;
      // Adjust increment speed based on how large the target is
      const increment = target > 100 ? Math.ceil(target / 60) : 1; 
      const stepTime = Math.abs(Math.floor(duration / (target / increment)));

      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        
        // Handle specific string formatting like "1m05", "1m68"
        if (prefix === '1m' && current < 10) {
          counter.innerText = prefix + '0' + current + suffix;
        } else {
          counter.innerText = prefix + current + suffix;
        }
      }, stepTime > 10 ? stepTime : 15); // limit minimum interval speed
    };

    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const counter = entry.target;
          // Chỉ đếm lên 1 lần khi cuộn tới
          if (!counter.classList.contains('counted')) {
            counter.classList.add('counted');
            animateCounter(counter);
          }
        }
      });
    }, { threshold: 0.5 }); // Trigger when 50% visible

    counters.forEach(counter => countObserver.observe(counter));
    console.log(`Count-up observer attached to ${counters.length} elements.`);
  }

  // --- Random Auto Hover Effect cho ảnh (Education & Why Me) ---
  const galleryImages = document.querySelectorAll('.bg-education img, .bg-why-me img');
  if (galleryImages.length > 0) {
    setInterval(() => {
      // Xóa class phát sáng ở tất cả các ảnh (để tránh lỗi dồn dập)
      galleryImages.forEach(img => img.classList.remove('auto-hover-glow'));
      
      // Chọn 1 ảnh ngẫu nhiên
      const randomIndex = Math.floor(Math.random() * galleryImages.length);
      const randomImg = galleryImages[randomIndex];
      
      // Thêm class phát sáng
      randomImg.classList.add('auto-hover-glow');
    }, 2000); // Cứ mỗi 2 giây lại đổi ảnh phát sáng
    console.log(`Random hover effect active on ${galleryImages.length} images.`);
  }
})();

// --- Stage Moments Filter Logic ---
window.filterMoments = function(category) {
  // Update active button state
  const buttons = document.querySelectorAll('.moments-filter .filter-btn');
  buttons.forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');

  // Filter items
  const items = document.querySelectorAll('.moment-item');
  items.forEach(item => {
    if (category === 'all' || item.getAttribute('data-category') === category) {
      item.classList.remove('hidden');
    } else {
      item.classList.add('hidden');
    }
  });
};

// --- Scroll To Top Logic ---
(function() {
  const scrollToTopBtn = document.getElementById('scrollToTopBtn');

  if (scrollToTopBtn) {
    window.addEventListener('scroll', () => {
      // Hiện nút khi cuộn quá 300px
      if (window.scrollY > 300) {
        scrollToTopBtn.classList.add('show');
      } else {
        scrollToTopBtn.classList.remove('show');
      }
    });

    scrollToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
})();

// --- Auto-scroll & Infinite Loop cho Testimonial Swipe Carousel (Mobile) ---
(function initTestimonialCarousel() {
  let attempts = 0;
  const checkInterval = setInterval(() => {
    const bento = document.querySelector('.testi-bento');
    if (bento) {
      clearInterval(checkInterval);
      
      // Khởi tạo Infinite Loop bằng cách nhân bản các item
      const originalItems = Array.from(bento.children);
      if (originalItems.length === 0) return;

      // Nhân bản 2 lần để có thể vuốt vô tận cả 2 chiều (trái/phải)
      originalItems.forEach(item => bento.appendChild(item.cloneNode(true)));
      originalItems.forEach(item => bento.appendChild(item.cloneNode(true)));

      // Chờ DOM cập nhật
      setTimeout(() => {
        // Disable smooth scroll trong CSS để jump không bị giật
        bento.style.scrollBehavior = 'auto';
        
        // Tính toán kích thước của 1 block gốc (6 items)
        const blockWidth = bento.scrollWidth / 3;
        
        // Di chuyển đến block giữa (để có thể lướt qua trái ngay lập tức)
        bento.scrollLeft = blockWidth;

        // Xử lý sự kiện scroll để tạo cảm giác vô tận (Seamless Loop)
        bento.addEventListener('scroll', () => {
          if (bento.scrollLeft >= blockWidth * 2 - 10) {
            // Chạm đến block cuối -> Nhảy về block giữa
            bento.scrollLeft -= blockWidth;
          } else if (bento.scrollLeft <= 0) {
            // Chạm đến block đầu -> Nhảy tới block giữa
            bento.scrollLeft += blockWidth;
          }
        });

        // Tự động cuộn (Auto-scroll) mỗi 3 giây thay vì 10s cho nhanh
        let autoScrollTimer;
        let isPaused = false;

        const startScroll = () => {
          clearInterval(autoScrollTimer);
          autoScrollTimer = setInterval(() => {
            if (!isPaused) {
              const item = bento.querySelector('.testi-item');
              const gap = parseFloat(getComputedStyle(bento).gap) || 16;
              const itemWidth = item.offsetWidth + gap;
              
              // Cuộn sang phải bằng JS smooth
              bento.scrollBy({ left: itemWidth, behavior: 'smooth' }); 
            }
          }, 3000); // Tăng tốc độ tự động lướt lên 3s để khách thấy hiệu ứng
        };

        startScroll();

        // Tạm dừng khi người dùng đang vuốt
        bento.addEventListener('touchstart', () => { isPaused = true; }, {passive: true});
        bento.addEventListener('touchend', () => { 
          setTimeout(() => { isPaused = false; }, 3000); 
        }, {passive: true});

      }, 100);

      console.log('Testimonial infinite auto-scroll initialized.');
    } else {
      attempts++;
      if (attempts > 20) clearInterval(checkInterval);
    }
  }, 500);
})();
