function setupDragToggle(container, toggleCallback) {
    let isDragging = false;
    let toggleState = null;
    let affectedItems = new Set();
    let startItem = null;

    function toggleAndRemember(item) {
        if (!affectedItems.has(item)) {
            toggleCallback(item, toggleState);
            affectedItems.add(item);
        }
    }

    container.addEventListener('mousedown', (e) => {
        const item = e.target.closest('.legend-item');
        if (item) {
            isDragging = true;
            startItem = item;
            toggleState = item.classList.contains('disabled');
            affectedItems.clear();
            toggleAndRemember(item);
        }
    });

    container.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const item = e.target.closest('.legend-item');
            if (item && item !== startItem) {
                toggleAndRemember(item);
            }
        }
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
        toggleState = null;
        affectedItems.clear();
        startItem = null;
    });
}

function applyDragToggleToLegend(legend, toggleRangeCallback) {
    setupDragToggle(legend, (item, shouldEnable) => {
        const label = item.getAttribute('data-label');
        toggleRangeCallback(label);
        if (shouldEnable) {
            item.classList.remove('disabled');
        } else {
            item.classList.add('disabled');
        }
    });
}