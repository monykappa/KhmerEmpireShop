document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/products/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('products-container');
            data.forEach(laptopSpec => {
                const productCard = document.createElement('div');
                productCard.className = 'col-md-4';

                // Check if images exist
                let images = '';
                if (laptopSpec.product.images.length > 0) {
                    images = `<img src="${laptopSpec.product.images[0].image}" alt="${laptopSpec.product.name}">`;
                } else {
                    images = `<img src="{% static 'placeholder_image.jpg' %}" alt="No image">`;
                }

                // GPU info
                let gpuInfo = 'N/A';
                if (laptopSpec.gpu.length > 0) {
                    gpuInfo = `${laptopSpec.gpu[0].gpu_brand.name} ${laptopSpec.gpu[0].model}`;
                }

                // Ensure 'slug' is available
                const productSlug = laptopSpec.slug;

                // Only create "See More" button if 'slug' is not null or undefined
                let seeMoreButton = '';
                if (productSlug !== null && productSlug !== undefined) {
                    seeMoreButton = `<a href="/products/${productSlug}" class="btn btn-primary">See More</a>`;
                }

                productCard.innerHTML = `
                    <div class="product-card">
                        ${images}
                        <h4>${laptopSpec.product.name} ${laptopSpec.product.model} ${laptopSpec.product.year}</h4>
                        <p><strong>CPU:</strong> ${laptopSpec.cpu.cpu_brand.name} ${laptopSpec.cpu.model} | ${gpuInfo} | ${laptopSpec.storage.capacity} ${laptopSpec.storage.capacity_type} | ${laptopSpec.memory.capacity}GB</p>
                        <h3 class="text-danger">$${laptopSpec.product.price}</h3>
                        ${seeMoreButton}
                    </div>
                `;
                container.appendChild(productCard);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});
