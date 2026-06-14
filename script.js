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
