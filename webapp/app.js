document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('card-grid');

    // Load data from global scope (injected by data.js)
    const demoData = window.demoData || [];

    if (demoData.length === 0) {
        console.warn('No demo data found in window.demoData');
        // Optional: show empty state or error in grid
        grid.innerHTML = '<div class="error-message">No data loaded. Please run extraction script.</div>';
    }

    renderCards(demoData);

    // Filter Logic
    window.filterCards = function (filterType) {
        const buttons = document.querySelectorAll('.filter-btn');
        const clickedBtn = document.querySelector(`.filter-btn.${filterType.replace(' ', '-')}`);

        // Toggle active state
        if (clickedBtn.classList.contains('active')) {
            // If already active, clear filter (show all)
            clickedBtn.classList.remove('active');
            renderCards(demoData);
        } else {
            // Activate clicked button, deactivate others
            buttons.forEach(btn => btn.classList.remove('active'));
            clickedBtn.classList.add('active');

            // Filter data
            const filtered = demoData.filter(item =>
                (item.actor || '').toLowerCase().includes(filterType)
            );
            renderCards(filtered);
        }
    };

    function renderCards(items) {
        grid.innerHTML = '';

        if (items.length === 0) {
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 50px;">No cards found matching filter.</div>';
            return;
        }

        items.forEach((item, index) => {
            // ... existing render logic ...
            const card = document.createElement('div');

            // Determine styling based on actor
            let actorClass = '';
            let iconHtml = '';

            // Normalize actor query
            const actorLower = (item.actor || '').toLowerCase();

            if (actorLower.includes('full demo')) {
                actorClass = 'actor-full-demo';
                // Desktop/Screen icon (SVG)
                iconHtml = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>`;
            } else if (actorLower.includes('presentation')) {
                actorClass = 'actor-presentation';
                // Presentation/Chart icon (SVG)
                iconHtml = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>`;
            } else {
                actorClass = 'default';
                // User icon
                iconHtml = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>`;
            }

            card.className = `card ${actorClass}`;
            card.style.animationDelay = `${index * 0.05}s`; // Staggered animation

            // Generate avatar content (Icon instead of initials if match, or initials)
            // Use iconHtml directly

            card.innerHTML = `
                <div class="card-header">
                    <span class="card-id">#${item.id}</span>
                    <span class="card-step">${item.step || 'Step'}</span>
                </div>
                <div class="card-body">
                    <h3>${item.action}</h3>
                </div>
                <div class="card-footer">
                    <div class="actor-avatar">
                        ${iconHtml}
                    </div>
                    <span class="actor-name">${item.actor || 'Unknown Actor'}</span>
                    <input type="checkbox" class="card-checkbox" title="Mark as complete">
                </div>
            `;

            // Add click listener for the checkbox
            // We need to do this after appending, or create element via DOM API
            // Let's create element via string first, then query inside the card element 
            // BUT card is not in DOM yet until grid.appendChild

            // Better approach: create card content, then find checkbox

            grid.appendChild(card);

            const checkbox = card.querySelector('.card-checkbox');
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    card.classList.add('completed');
                } else {
                    card.classList.remove('completed');
                }
            });
        });
    }
});
