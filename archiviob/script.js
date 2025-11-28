// Configuration - adjust these as needed
const MAX_NUMBERS = 10; // Maximum number to check (01 to MAX_NUMBERS)
const LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']; // Letters to check
const IMAGE_EXTENSIONS = ['.jpg']; // Supported formats

// Global variable to store all images grouped by number
let imagesByNumber = {};
let allExistingImages = [];

// Function to generate all possible image paths
function generateImagePaths() {
    const imagePaths = [];
    
    for (let num = 1; num <= MAX_NUMBERS; num++) {
        const paddedNum = String(num).padStart(2, '0');
        
        for (const letter of LETTERS) {
            const baseName = `${paddedNum}_${letter}`;
            // Try all extensions
            for (const ext of IMAGE_EXTENSIONS) {
                imagePaths.push({
                    path: `pictures/${baseName}${ext}`,
                    number: paddedNum,
                    letter: letter
                });
            }
        }
    }
    
    return imagePaths;
}

// Function to check if image exists
async function imageExists(path) {
    return new Promise((resolve) => {
        const img = new Image();
        const timeout = setTimeout(() => {
            img.src = '';
            resolve(false);
        }, 3000); // 3 second timeout
        
        img.onload = () => {
            clearTimeout(timeout);
            resolve(true);
        };
        img.onerror = () => {
            clearTimeout(timeout);
            resolve(false);
        };
        // Set decoding to async for better performance
        img.decoding = 'async';
        img.src = path;
    });
}

// Function to shuffle array (Fisher-Yates algorithm)
function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Function to load all images
async function loadGallery() {
    const gallery = document.getElementById('gallery');
    
    // Generate all possible paths
    const allPossiblePaths = generateImagePaths();
    
    // Split into first batch (immediate) and rest (async)
    const firstBatch = allPossiblePaths.slice(0, 10);
    const restBatch = allPossiblePaths.slice(10);
    
    // Check first 10 images immediately
    const firstResults = await Promise.all(
        firstBatch.map(async imageInfo => {
            const exists = await imageExists(imageInfo.path);
            return exists ? imageInfo : null;
        })
    );
    
    const existingImages = firstResults.filter(img => img !== null);
    
    // Check and load remaining images asynchronously
    Promise.all(
        restBatch.map(async imageInfo => {
            const exists = await imageExists(imageInfo.path);
            return exists ? imageInfo : null;
        })
    ).then(restResults => {
        const moreImages = restResults.filter(img => img !== null);
        existingImages.push(...moreImages);
        
        // Store all images globally
        allExistingImages = existingImages;
        
        // Group images by number
        imagesByNumber = {};
        existingImages.forEach(imageInfo => {
            if (!imagesByNumber[imageInfo.number]) {
                imagesByNumber[imageInfo.number] = [];
            }
            imagesByNumber[imageInfo.number].push(imageInfo);
        });
        
        // Sort images within each group by letter
        Object.keys(imagesByNumber).forEach(number => {
            imagesByNumber[number].sort((a, b) => a.letter.localeCompare(b.letter));
        });
        
        // Randomize ALL images together and render once
        gallery.innerHTML = '';
        renderImages(existingImages, gallery, true);
    });
}

function renderImages(images, gallery, randomize = false) {
    // Randomize if requested
    const imagesToRender = randomize ? shuffleArray(images) : images;
    
    // Use document fragment for better performance
    const fragment = document.createDocumentFragment();
    
    imagesToRender.forEach((imageInfo) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'image-wrapper';
        wrapper.dataset.number = imageInfo.number;
        wrapper.dataset.letter = imageInfo.letter;
        
        // Add click event to open slideshow
        wrapper.addEventListener('click', () => openSlideshow(imageInfo.number, imageInfo.letter), { passive: true });
        
        const img = document.createElement('img');
        img.src = imageInfo.path;
        img.alt = `Image ${imageInfo.number}`;
        img.decoding = 'async';
        
        const numberLabel = document.createElement('div');
        numberLabel.className = 'image-number';
        numberLabel.textContent = imageInfo.number;
        
        wrapper.appendChild(img);
        wrapper.appendChild(numberLabel);
        fragment.appendChild(wrapper);
    });
    
    gallery.appendChild(fragment);
}

// Slideshow functionality
let currentSlideIndex = 0;
let currentGroup = [];

function openSlideshow(number, clickedLetter) {
    currentGroup = imagesByNumber[number] || [];
    
    if (currentGroup.length === 0) return;
    
    // Find the index of the clicked image letter in the group
    currentSlideIndex = currentGroup.findIndex(img => img.letter === clickedLetter);
    if (currentSlideIndex === -1) currentSlideIndex = 0;
    
    showSlide(currentSlideIndex);
    
    const slideshow = document.getElementById('slideshow');
    slideshow.style.display = 'flex';
    
    // Trigger reflow to enable transition
    setTimeout(() => {
        slideshow.classList.add('active');
    }, 10);
}

function closeSlideshow() {
    const slideshow = document.getElementById('slideshow');
    slideshow.classList.remove('active');
    
    setTimeout(() => {
        slideshow.style.display = 'none';
    }, 300);
}

function showSlide(index) {
    if (currentGroup.length === 0) return;
    
    // Ensure index is within bounds
    currentSlideIndex = Math.max(0, Math.min(index, currentGroup.length - 1));
    
    const slideshowImage = document.getElementById('slideshowImage');
    const newImagePath = currentGroup[currentSlideIndex].path;
    
    // Preload next and previous images for smoother navigation
    if (currentSlideIndex + 1 < currentGroup.length) {
        const nextImg = new Image();
        nextImg.src = currentGroup[currentSlideIndex + 1].path;
    }
    if (currentSlideIndex - 1 >= 0) {
        const prevImg = new Image();
        prevImg.src = currentGroup[currentSlideIndex - 1].path;
    }
    
    slideshowImage.src = newImagePath;
}

function nextSlide() {
    currentSlideIndex = (currentSlideIndex + 1) % currentGroup.length;
    showSlide(currentSlideIndex);
}

function prevSlide() {
    currentSlideIndex = (currentSlideIndex - 1 + currentGroup.length) % currentGroup.length;
    showSlide(currentSlideIndex);
}

// Event listeners for slideshow
document.getElementById('closeSlideshow').addEventListener('click', closeSlideshow, { passive: true });

// Click zones: left = previous, right = next
document.getElementById('clickZoneLeft').addEventListener('click', (e) => {
    e.stopPropagation();
    prevSlide();
}, { passive: true });

document.getElementById('clickZoneRight').addEventListener('click', (e) => {
    e.stopPropagation();
    nextSlide();
}, { passive: true });

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    const slideshow = document.getElementById('slideshow');
    if (!slideshow.classList.contains('active')) return;
    
    if (e.key === 'Escape') {
        closeSlideshow();
    } else if (e.key === 'ArrowRight') {
        nextSlide();
    } else if (e.key === 'ArrowLeft') {
        prevSlide();
    }
});

// Close slideshow when clicking outside the image or on background
document.getElementById('slideshow').addEventListener('click', (e) => {
    // Close if clicking on the slideshow background or the content area (not click zones or image)
    if (e.target.id === 'slideshow' || e.target.classList.contains('slideshow-content')) {
        closeSlideshow();
    }
});

// Touch/swipe support for mobile
let touchStartX = 0;
let touchEndX = 0;
const minSwipeDistance = 50; // minimum distance for a swipe

document.getElementById('slideshow').addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

document.getElementById('slideshow').addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
}, { passive: true });

function handleSwipe() {
    const swipeDistance = touchEndX - touchStartX;
    
    if (Math.abs(swipeDistance) < minSwipeDistance) {
        return; // Not a swipe, just a tap
    }
    
    if (swipeDistance > 0) {
        // Swiped right -> previous slide
        prevSlide();
    } else {
        // Swiped left -> next slide
        nextSlide();
    }
}

// Load gallery when page loads
document.addEventListener('DOMContentLoaded', loadGallery);
