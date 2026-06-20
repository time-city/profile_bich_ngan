/* Fade-in removed to improve performance */

  // --- Autoplay Videos on Scroll & Prevent Black Screen ---
  const videoElements = document.querySelectorAll('video');
  if (videoElements.length > 0) {
    const videoObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.play().catch(e => console.log("Autoplay prevented by browser:", e));
        } else {
          entry.target.pause();
        }
      });
    }, { threshold: 0.2 });

    videoElements.forEach(video => {
      video.muted = true;
      video.playsInline = true;
      
      // Mẹo chống đen màn hình trên mobile khi chưa play:
      // Ép video nhảy tới 0.1s để load frame đầu tiên
      if (video.readyState >= 1) {
        video.currentTime = 0.1;
      } else {
        video.addEventListener('loadedmetadata', function() {
          this.currentTime = 0.1;
        }, { once: true });
      }

      videoObserver.observe(video);
    });
    
    console.log(`Video observer attached to ${videoElements.length} videos.`);
  }

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
  const galleryImages = document.querySelectorAll('.bg-why-me img');
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

// --- Auto-play Videos on Scroll & Single Play Logic ---
(function initVideoLogic() {
  let attempts = 0;
  const checkInterval = setInterval(() => {
    const videos = Array.from(document.querySelectorAll('video'));
    if (videos.length > 0) {
      clearInterval(checkInterval);

      // Track which videos are visible to prevent race conditions on mobile
      const visibleVideos = new Set();

      const videoObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          const video = entry.target;
          if (entry.isIntersecting) {
            visibleVideos.add(video);
          } else {
            visibleVideos.delete(video);
            video.pause();
          }
        });

        // Determine if we need to auto-play a video
        let hasPlaying = false;
        videos.forEach(v => {
          if (visibleVideos.has(v) && !v.paused) hasPlaying = true;
        });

        // Only auto-play the FIRST visible video if none are playing
        if (!hasPlaying && visibleVideos.size > 0) {
          for (let video of videos) {
            if (visibleVideos.has(video)) {
              video.muted = true;
              video.play().catch(e => console.log('Autoplay blocked by browser:', e));
              break; // Stop after playing one
            }
          }
        }
      }, { threshold: 0.1 }); // Kích hoạt ngay khi video lộ ra 10%

      videos.forEach(video => {
        // Đảm bảo các thuộc tính bắt buộc cho mobile
        video.setAttribute('playsinline', '');
        video.setAttribute('muted', '');
        videoObserver.observe(video);

        // Chỉ cho phép 1 video play cùng lúc khi click thủ công
        video.addEventListener('play', () => {
          videos.forEach(v => {
            if (v !== video && !v.paused) {
              v.pause();
            }
          });
        });
      });

      console.log('Video auto-play and single-play logic initialized.');
    } else {
      attempts++;
      if (attempts > 40) clearInterval(checkInterval);
    }
  }, 500);
})();
