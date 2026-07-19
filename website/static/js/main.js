document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById('site-header');
    const mobileToggle = document.querySelector('.mobile-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    let lastScroll = 0;
    const handleScroll = () => {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        lastScroll = currentScroll;
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', () => {
            const isExpanded = mobileToggle.getAttribute('aria-expanded') === 'true';
            mobileToggle.setAttribute('aria-expanded', !isExpanded);
            mobileMenu.classList.toggle('active');
            mobileMenu.setAttribute('aria-hidden', isExpanded);
            document.body.style.overflow = isExpanded ? '' : 'hidden';
        });

        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileToggle.setAttribute('aria-expanded', 'false');
                mobileMenu.classList.remove('active');
                mobileMenu.setAttribute('aria-hidden', 'true');
                document.body.style.overflow = '';
            });
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const headerOffset = header.offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerOffset;
                window.scrollTo({ top: targetPosition, behavior: 'smooth' });
            }
        });
    });

    const modals = document.querySelectorAll('.modal');
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modalClosers = document.querySelectorAll('[data-close-modal]');

    const openModal = (modalId) => {
        const modal = document.getElementById(modalId);
        if (!modal) return;
        modal.hidden = false;
        modal.offsetHeight;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        const firstInput = modal.querySelector('input, textarea, select');
        if (firstInput) setTimeout(() => firstInput.focus(), 100);
    };

    const closeModal = (modal) => {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.hidden = true;
            document.body.style.overflow = '';
        }, 300);
    };

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = trigger.dataset.modal;
            if (modalId) openModal(modalId);
        });
    });

    modalClosers.forEach(closer => {
        closer.addEventListener('click', () => {
            const modal = closer.closest('.modal');
            if (modal) closeModal(modal);
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            modals.forEach(modal => {
                if (modal.classList.contains('active')) closeModal(modal);
            });
            const lightbox = document.getElementById('lightbox');
            if (lightbox && lightbox.classList.contains('active')) closeLightbox();
        }
    });

    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.classList.contains('modal-overlay')) {
                closeModal(modal);
            }
        });
    });

    const handleFormSubmit = async (form, endpoint) => {
        const submitBtn = form.querySelector('button[type="submit"]');
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        const messageEl = form.querySelector('.form-message');

        submitBtn.disabled = true;
        if (btnText) btnText.hidden = true;
        if (btnLoader) btnLoader.hidden = false;

        try {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                messageEl.textContent = result.message;
                messageEl.className = 'form-message success';
                messageEl.hidden = false;
                form.reset();
            } else {
                throw new Error(result.error || 'Something went wrong');
            }
        } catch (error) {
            messageEl.textContent = error.message || 'Failed to send. Please try again or call us directly.';
            messageEl.className = 'form-message error';
            messageEl.hidden = false;
        } finally {
            submitBtn.disabled = false;
            if (btnText) btnText.hidden = false;
            if (btnLoader) btnLoader.hidden = true;
        }
    };

    const inspectionForm = document.getElementById('inspection-form');
    if (inspectionForm) {
        inspectionForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(inspectionForm, '/api/inspection-request');
        });
    }

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(contactForm, '/api/contact');
        });
    }

    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightbox-image');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const lightboxCounter = document.getElementById('lightbox-counter');
    const lightboxClose = document.querySelector('.lightbox-close');
    const lightboxPrev = document.querySelector('.lightbox-prev');
    const lightboxNext = document.querySelector('.lightbox-next');

    let galleryItems = [];
    let currentIndex = 0;

    const updateGalleryItems = () => {
        galleryItems = Array.from(document.querySelectorAll('.gallery-item, .gallery-masonry-item'));
    };

    const openLightbox = (index) => {
        if (!galleryItems.length) updateGalleryItems();
        if (!galleryItems.length) return;

        currentIndex = index;
        const item = galleryItems[index];
        lightboxImage.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="800" height="600"%3E%3Crect fill="%23e2e8f0" width="800" height="600"/%3E%3Ctext fill="%235C6670" font-family="sans-serif" font-size="24" x="50%25" y="50%25" text-anchor="middle" dominant-baseline="middle"%3EPlaceholder Image%3C/text%3E%3C/svg%3E';
        lightboxImage.alt = item.querySelector('figcaption')?.textContent || 'Gallery image';
        lightboxCaption.textContent = item.querySelector('figcaption')?.textContent || '';
        lightboxCounter.textContent = (index + 1) + ' / ' + galleryItems.length;

        lightbox.hidden = false;
        lightbox.offsetHeight;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    const closeLightbox = () => {
        lightbox.classList.remove('active');
        setTimeout(() => {
            lightbox.hidden = true;
            document.body.style.overflow = '';
        }, 300);
    };

    const showPrev = () => {
        currentIndex = (currentIndex - 1 + galleryItems.length) % galleryItems.length;
        openLightbox(currentIndex);
    };

    const showNext = () => {
        currentIndex = (currentIndex + 1) % galleryItems.length;
        openLightbox(currentIndex);
    };

    const initGallery = () => {
        updateGalleryItems();
        galleryItems.forEach((item, index) => {
            item.addEventListener('click', () => openLightbox(index));
        });
    };

    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    if (lightboxPrev) lightboxPrev.addEventListener('click', (e) => { e.stopPropagation(); showPrev(); });
    if (lightboxNext) lightboxNext.addEventListener('click', (e) => { e.stopPropagation(); showNext(); });
    if (lightbox) {
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) closeLightbox();
        });
    }

    initGallery();

    const filterBtns = document.querySelectorAll('.gallery-filter-btn');
    const masonryItems = document.querySelectorAll('.gallery-masonry-item');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.dataset.filter;
            filterBtns.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');

            masonryItems.forEach(item => {
                const categories = item.dataset.category?.split(' ') || [];
                if (filter === 'all' || categories.includes(filter)) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
        });
    });

    const revealElements = document.querySelectorAll('.service-card, .why-card, .trust-item, .gallery-item, .area-card, .faq-item, .pricing-card');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(el => {
        el.classList.add('reveal');
        revealObserver.observe(el);
    });
});
