/* Fade-in removed to improve performance */

  // --- Legacy Video Autoplay removed to allow Custom Controls ---

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

// --- Legacy Auto-play Videos on Scroll Logic Removed ---

// --- Custom Video Controls Logic ---
document.addEventListener('click', function(e) {
  // Check if click is on or within a custom video button
  const btn = e.target.closest('.vid-btn');
  if (!btn) return;

  const wrapper = btn.closest('.vid-wrapper');
  if (!wrapper) return;

  const video = wrapper.querySelector('video');
  if (!video) return;

  // Prevent default behavior to avoid scrolling
  e.preventDefault();

  if (btn.classList.contains('play-pause')) {
    if (video.paused) {
      video.play();
      const iconPlay = btn.querySelector('.icon-play');
      const iconPause = btn.querySelector('.icon-pause');
      if (iconPlay) iconPlay.style.display = 'none';
      if (iconPause) iconPause.style.display = 'block';
    } else {
      video.pause();
      const iconPlay = btn.querySelector('.icon-play');
      const iconPause = btn.querySelector('.icon-pause');
      if (iconPlay) iconPlay.style.display = 'block';
      if (iconPause) iconPause.style.display = 'none';
    }
  } 
  else if (btn.classList.contains('mute')) {
    video.muted = !video.muted;
    if (video.muted) {
      btn.querySelector('.icon-unmute').style.display = 'none';
      btn.querySelector('.icon-mute').style.display = 'block';
    } else {
      btn.querySelector('.icon-unmute').style.display = 'block';
      btn.querySelector('.icon-mute').style.display = 'none';
    }
  }
  else if (btn.classList.contains('seek') && btn.classList.contains('backward')) {
    video.currentTime = Math.max(0, video.currentTime - 5);
  }
  else if (btn.classList.contains('seek') && btn.classList.contains('forward')) {
    video.currentTime = Math.min(video.duration, video.currentTime + 5);
  }
});

// Allow clicking the video itself to play/pause
document.addEventListener('click', function(e) {
  if (e.target.tagName === 'VIDEO') {
    const video = e.target;
    if (video.muted) {
      video.muted = false;
      if (video.paused) video.play();
    } else {
      if (video.paused) {
        video.play();
      } else {
        video.pause();
      }
    }
  }
});

// Sync Play/Pause icons and enforce single-play (pause others) when a video starts playing
document.addEventListener('play', function(e) {
  if (e.target.tagName === 'VIDEO') {
    const currentVideo = e.target;
    
    // Pause all other videos
    document.querySelectorAll('video').forEach(v => {
      if (v !== currentVideo && !v.paused) {
        v.pause();
      }
    });

    const wrapper = currentVideo.closest('.vid-wrapper');
    if (wrapper) {
      wrapper.classList.add('playing');
      const btn = wrapper.querySelector('.play-pause');
      if (btn) {
        const iconPlay = btn.querySelector('.icon-play');
        const iconPause = btn.querySelector('.icon-pause');
        if (iconPlay) iconPlay.style.display = 'none';
        if (iconPause) iconPause.style.display = 'block';
      }
    }
  }
}, true);

document.addEventListener('pause', function(e) {
  if (e.target.tagName === 'VIDEO') {
    const wrapper = e.target.closest('.vid-wrapper');
    if (wrapper) {
      wrapper.classList.remove('playing');
      const btn = wrapper.querySelector('.play-pause');
      if (btn) {
        const iconPlay = btn.querySelector('.icon-play');
        const iconPause = btn.querySelector('.icon-pause');
        if (iconPlay) iconPlay.style.display = 'block';
        if (iconPause) iconPause.style.display = 'none';
      }
    }
  }
}, true);

// Lazy Load Videos via Thumbnail Click or IntersectionObserver
document.addEventListener('click', function(e) {
  const btn = e.target.closest('.vid-thumbnail-btn');
  if(btn || e.target.closest('.vid-thumbnail')) {
    const thumbContainer = e.target.closest('.vid-thumbnail');
    if (!thumbContainer) return;
    
    let video = thumbContainer.querySelector('video');
    
    if (!video) {
      const src = thumbContainer.getAttribute('data-video-src');
      if(!src) return;
      
      // Load video on click if not already loaded by observer. Remove muted to allow sound when explicitly clicked.
      const posterSrc = thumbContainer.getAttribute('data-poster') || '';
      const videoHTML = `<video src=\"${src}\" poster=\"${posterSrc}\" autoplay playsinline style=\"width:100%; height:100%; object-fit:cover; border-radius:8px; background:#000;\"></video>`;
      thumbContainer.innerHTML = videoHTML;
      video = thumbContainer.querySelector('video');
    } else {
      if (video.paused) {
        video.play();
        video.muted = false; // Unmute on explicit interaction
      }
    }
  }
});

// --- Auto Play/Pause Videos based on Viewport Visibility (TikTok/Reels style) ---
if ('IntersectionObserver' in window) {
  const videoObserverOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.6 // Trigger when 60% of the video is visible
  };

  window.videoObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const thumbContainer = entry.target;
      
      if (entry.isIntersecting) {
        // Play the video
        let video = thumbContainer.querySelector('video');
        if (!video) {
          // If video element doesn't exist yet, create it automatically
          const src = thumbContainer.getAttribute('data-video-src');
          if (src) {
            // Must be muted for mobile autoplay
            const posterSrc = thumbContainer.getAttribute('data-poster') || '';
            const videoHTML = `<video src="${src}" poster="${posterSrc}" autoplay playsinline muted loop style="width:100%; height:100%; object-fit:cover; border-radius:8px; background:#000; pointer-events: none;"></video>`;
            thumbContainer.innerHTML = videoHTML;
            video = thumbContainer.querySelector('video');
          }
        }
        
        if (video) {
          // Attempt to play with sound
          video.muted = false;
          video.play().catch(e => {
            console.log("Unmuted autoplay prevented:", e);
            // Browser strictly requires muted autoplay on scroll. 
            // Fallback to muted to ensure video actually plays instead of freezing at 0:00.
            video.muted = true;
            video.play().catch(err => console.log("Muted autoplay also failed:", err));
          });
        }
      } else {
        // Pause the video when it goes out of view
        const video = thumbContainer.querySelector('video');
        if (video && !video.paused) {
          video.pause();
        }
      }
    });
  }, videoObserverOptions);

  // Observe all video thumbnails immediately since this script is injected after content load
  const thumbnails = document.querySelectorAll('.vid-thumbnail, .vid-wrapper, .project-video');
  thumbnails.forEach(thumb => {
    window.videoObserver.observe(thumb);
  });
}

// Dynamically correct video aspect ratio containers on load
// We can't immediately check video dimensions without loading them.
// Let's create an invisible video element to sniff the actual dimensions for any thumbnail.
(function() {
  const thumbnails = document.querySelectorAll('.vid-thumbnail, .vid-wrapper');
  thumbnails.forEach(thumb => {
    const src = thumb.getAttribute('data-video-src');
    if (!src) return;
    
    const v = document.createElement('video');
    v.preload = 'metadata';
    v.src = src;
    v.onloadedmetadata = () => {
      // If browser detects video height > width, force it to be vertical container
      if (v.videoHeight > v.videoWidth) {
        if (!thumb.classList.contains('vid-vertical')) {
          thumb.classList.add('vid-vertical');
        }
      } else {
        if (thumb.classList.contains('vid-vertical')) {
          thumb.classList.remove('vid-vertical');
        }
      }
    };
  });
})();

// --- Auto-scroll cho Video Gallery (Mobile) ---
(function initVideoGalleryAutoScroll() {
  let attempts = 0;
  const checkInterval = setInterval(() => {
    const galleries = document.querySelectorAll('.video-gallery-grid');
    if (galleries.length > 0) {
      clearInterval(checkInterval); // Stop checking once found

      // Đợi thêm một chút để đảm bảo DOM layout đã hoàn tất
      setTimeout(() => {
          galleries.forEach((gallery, index) => {
            if (gallery.dataset.autoScrollInit) return;
            
            // Only auto-scroll on mobile where it's a horizontally scrollable flex container
            if (window.innerWidth > 768) return; 

            gallery.dataset.autoScrollInit = 'true';

            // Nhân bản các item để tạo vòng lặp vô tận (Infinite Loop)
            const originalItems = Array.from(gallery.children);
            if (originalItems.length <= 2) {
                gallery.style.justifyContent = 'center';
                return;
            }

            // Clone 2 lần để đảm bảo vuốt được hai chiều
            originalItems.forEach(item => {
                const clone = item.cloneNode(true);
                gallery.appendChild(clone);
                // Đăng ký lại observer cho các thumbnail mới
                const thumbs = clone.querySelectorAll('.vid-thumbnail');
                if (window.videoObserver) {
                    thumbs.forEach(thumb => window.videoObserver.observe(thumb));
                }
            });
            originalItems.forEach(item => {
                const clone = item.cloneNode(true);
                gallery.appendChild(clone);
                const thumbs = clone.querySelectorAll('.vid-thumbnail');
                if (window.videoObserver) {
                    thumbs.forEach(thumb => window.videoObserver.observe(thumb));
                }
            });

            // Chiều cuộn luân phiên: 
            // index chẵn (VD: 0, 2): trái sang phải (scrollLeft giảm) => dir = -1
            // index lẻ (VD: 1, 3): phải sang trái (scrollLeft tăng) => dir = 1
            const dir = index % 2 === 0 ? -1 : 1; 

            // Tính toán kích thước của 1 block gốc ban đầu
            const blockWidth = gallery.scrollWidth / 3;

            // Thiết lập vị trí cuộn ban đầu ở giữa để có thể cuộn vô tận hai chiều
            gallery.style.scrollBehavior = 'auto'; // Tắt mượt để nhảy ngay lập tức
            gallery.scrollLeft = blockWidth;

            let isTouching = false;
            let playingCount = 0;
            let speed = 0.5; // Tốc độ trôi (pixel mỗi frame)
            let currentScrollLeftFloat = blockWidth;
            let touchTimeout;

            const scrollLoop = () => {
                if (!isTouching && playingCount === 0) {
                    const currentBlockWidth = gallery.scrollWidth / 3;
                    
                    // Đồng bộ nếu người dùng vừa vuốt tay
                    if (Math.abs(currentScrollLeftFloat - gallery.scrollLeft) > 5) {
                        currentScrollLeftFloat = gallery.scrollLeft;
                    }

                    // Xử lý Seamless Jump (vòng lặp vô cực)
                    if (dir === 1) { // Đang cuộn sang trái (phải sang trái màn hình)
                        if (currentScrollLeftFloat >= currentBlockWidth * 2 - 10) {
                            currentScrollLeftFloat -= currentBlockWidth;
                        }
                        currentScrollLeftFloat += speed;
                    } else { // Đang cuộn sang phải (trái sang phải màn hình)
                        if (currentScrollLeftFloat <= 10) {
                            currentScrollLeftFloat += currentBlockWidth;
                        }
                        currentScrollLeftFloat -= speed;
                    }

                    gallery.scrollLeft = currentScrollLeftFloat;
                } else {
                    currentScrollLeftFloat = gallery.scrollLeft;
                }
                requestAnimationFrame(scrollLoop);
            };

            // Trì hoãn một chút trước khi chạy
            setTimeout(() => {
                gallery.style.scrollSnapType = 'none'; // Tắt snap để trôi mượt liên tục
                requestAnimationFrame(scrollLoop);
            }, 500);

            // Tạm dừng tự động cuộn khi người dùng chạm vuốt
            gallery.addEventListener('touchstart', () => { 
                isTouching = true; 
                gallery.style.scrollSnapType = ''; // Bật lại snap để vuốt tay có khấc
                clearTimeout(touchTimeout);
            }, {passive: true});
            
            gallery.addEventListener('touchend', () => { 
                clearTimeout(touchTimeout);
                touchTimeout = setTimeout(() => { 
                    isTouching = false; 
                    if (playingCount === 0) gallery.style.scrollSnapType = 'none'; // Tắt snap lại để tự chạy
                }, 2000); 
            }, {passive: true});
            
            // Dừng cuộn khi xem video
            gallery.addEventListener('play', (e) => {
               if (e.target.tagName === 'VIDEO') {
                   playingCount++;
                   gallery.style.scrollSnapType = ''; // Bật snap giữ video ở giữa màn hình
               }
            }, true);
            
            gallery.addEventListener('pause', (e) => {
               if (e.target.tagName === 'VIDEO') {
                   playingCount = Math.max(0, playingCount - 1);
                   if (playingCount === 0 && !isTouching) {
                       gallery.style.scrollSnapType = 'none'; // Trôi tiếp
                   }
               }
            }, true);
          });
      }, 500);
      
    } else {
      attempts++;
      if (attempts > 20) clearInterval(checkInterval);
    }
  }, 500);
})();

