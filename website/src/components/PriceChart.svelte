<script lang="ts">
    import { onMount } from 'svelte';
    import {Chart, type ChartType, registerables} from 'chart.js';
    import 'chartjs-adapter-date-fns';
    import { enUS } from 'date-fns/locale';

    let priceData: { name: string, price: { [date: string]: number } }[] = [];
    let selectedGroceries: string[] = [];

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
        return data
            .map(item => {
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
                const chart = new Chart(ctx, {
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

                document.querySelectorAll<HTMLInputElement>('input[type="checkbox"]').forEach(checkbox => {
                    checkbox.addEventListener('change', () => {
                        selectedGroceries = Array.from(document.querySelectorAll<HTMLInputElement>('input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
                        updateChart(chart, selectedGroceries);
                    });
                });
            } else {
                console.error('Failed to get 2D rendering context for canvas element');
            }
        } else {
            console.error('Canvas element not found');
        }
    });

    function updateChart(chart: Chart<ChartType, { x: string; y: number }[], unknown>, selectedGroceries: string[]): void {
        // Filter data based on selected groceries
        const filteredData = priceData.filter(item => selectedGroceries.includes(item.name));
        const chartData = transformData(filteredData);

        // Update chart data
        chart.data.datasets = chartData;
        chart.update();
    }
</script>

<div>
    {#each priceData as item}
        <label>
            <input type="checkbox" value={item.name} checked={selectedGroceries.includes(item.name)} />
            {item.name}
        </label>
    {/each}
</div>
<canvas id="priceChart" width="400" height="400"></canvas>

<!--<svelte:head>-->
<!--    <script>-->
<!--        fetchPriceData(); // Fetch data when the component is mounted-->
<!--    </script>-->
<!--</svelte:head>-->
