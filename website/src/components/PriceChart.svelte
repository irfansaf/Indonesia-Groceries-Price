<script lang="ts">
    import { onMount } from 'svelte';
    import { Chart, registerables } from 'chart.js';
    import 'chartjs-adapter-date-fns';
    import { enUS } from 'date-fns/locale';

    let priceData: { name: string, price: { [date: string]: number } }[] = [];

    async function fetchPriceData() {
        try {
            const response = await fetch('http://127.0.0.1:5000/price');
            const data = await response.json();
            priceData = data.groceries;
        } catch (error) {
            console.error('Error fetching price data:', error);
        }
    }

    function transformData(data: { name: string, price: { [date: string]: number } }[]) {
        return data.map(item => {
            const prices = Object.entries(item.price).map(([date, price]) => ({ x: date, y: price }));
            return { label: item.name, data: prices };
        });
    }

    onMount(async () => {
        const {default: ZoomPlugin} = await import('chartjs-plugin-zoom');

        await fetchPriceData();

        const chartData = transformData(priceData);

        Chart.register(ZoomPlugin, ...registerables);

        const canvas = document.getElementById('priceChart');

        if (canvas instanceof HTMLCanvasElement) {
            const ctx = canvas.getContext('2d');

            if (ctx) {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        datasets: chartData
                    },
                    options: {
                        scales: {
                            x: {
                                type: 'time',
                                adapters: {
                                    date: {
                                        locale: enUS
                                    }
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Price (IDR)'
                                }
                            }
                        },
                        plugins: {
                            zoom: {
                                zoom: {
                                    wheel: {
                                        enabled: true
                                    },
                                    pinch: {
                                        enabled: true
                                    },
                                    mode: 'xy'
                                },
                                pan: {
                                    enabled: true,
                                    mode: 'xy'
                                }
                            }
                        }
                    }
                });
            } else {
                console.error('Failed to get 2D rendering context for canvas element');
            }
        } else {
            console.error('Canvas element not found');
        }
    });
</script>

<canvas id="priceChart" width="400" height="400"></canvas>

<svelte:head>
    <script>
        fetchPriceData(); // Fetch data when the component is mounted
    </script>
</svelte:head>
