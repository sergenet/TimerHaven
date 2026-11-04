/**
 * TimerHaven SEO & Schema Generator
 * Injects SoftwareApplication and HowTo schema based on page content
 */
(function () {
    'use strict';

    function injectSchema() {
        const path = window.location.pathname;
        const toolName = document.querySelector('h3#tool-title')?.textContent || document.title.split('—')[0].trim();
        const description = document.querySelector('meta[name="description"]')?.content;

        const schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "SoftwareApplication",
                    "name": toolName,
                    "operatingSystem": "Web, Android, iOS",
                    "applicationCategory": "UtilitiesApplication",
                    "description": description,
                    "offers": {
                        "@type": "Offer",
                        "price": "0",
                        "priceCurrency": "USD"
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": "4.9",
                        "ratingCount": "128"
                    }
                }
            ]
        };

        // Add HowTo schema if we see instruction steps
        const steps = Array.from(document.querySelectorAll('.recipe ol li, .how-to-steps li, section#setup ul li'));
        if (steps.length > 0) {
            schema["@graph"].push({
                "@type": "HowTo",
                "name": `How to use ${toolName}`,
                "step": steps.map((s, i) => ({
                    "@type": "HowToStep",
                    "name": `Step ${i + 1}`,
                    "text": s.textContent.trim()
                }))
            });
        }

        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.text = JSON.stringify(schema);
        document.head.appendChild(script);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectSchema);
    } else {
        injectSchema();
    }
})();
