<script lang="ts">
    import {onMount} from 'svelte';
    import {Chart, type ChartType, registerables} from 'chart.js';
    import 'chartjs-adapter-date-fns';
    import { enUS } from 'date-fns/locale';

    let priceData: { name: string, price: { [date: string]: number }, category: string }[] = [];
    let selectedGroceries: string[] = [];

    async function fetchPriceData() {
        try {
            const response = await fetch('http://127.0.0.1:5000/price');
            const data = await response.json();
            priceData = data.groceries;
            selectedGroceries = priceData.map(item => item.name);
        } catch (error) {
            console.error('Error fetching price data:', error);
        }
    }

    function transformData(data: { name: string, price: { [date: string]: number }, category: string }[]) {
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

                // updateChart(chart, selectedGroceries);

                document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                    checkbox.addEventListener('change', () => {
                        selectedGroceries = Array.from(document.querySelectorAll<HTMLInputElement>('input[type="checkbox"]:checked')).map(checkbox => checkbox.value);
                        updateChart(chart, selectedGroceries);
                    });
                });

                // Select All
                document.getElementById('selectAll')?.addEventListener('change', (event) => {
                    const isChecked = (event.target as HTMLInputElement).checked;
                    document.querySelectorAll<HTMLInputElement>('input[type="checkbox"]').forEach(checkbox => {
                        checkbox.checked = isChecked;
                    });
                    selectedGroceries = isChecked ? priceData.map(item => item.name) : [];
                    updateChart(chart, selectedGroceries);
                });


                document.getElementById('groceriesDropdown')?.addEventListener('change', (event) => {
                    const selectedGroceries = Array.from((event.target as HTMLSelectElement).selectedOptions).map(option => option.value);

                    document.querySelectorAll<HTMLInputElement>('input[type="checkbox"]').forEach(checkbox => {
                        checkbox.checked = selectedGroceries.includes(checkbox.value);
                    });

                    updateChart(chart, selectedGroceries);
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

<div class="flex flex-col h-screen">
    <!-- Navbar -->
    <nav class="bg-gray-900 text-white p-4">
        <!-- Navbar content goes here -->
        <h1 class="text-2xl">Indonesia Groceries Price History</h1>
    </nav>

    <!-- Main content area -->
    <div class="flex flex-1">
        <!-- Left column for charts -->
        <div class="w-3/4 p-4">
            <div class="mb-4">
                <select id="groceriesDropdown" bind:value={selectedGroceries} class="p-2 border rounded-md">
                    <option value="" disabled>Select Groceries</option>
                    {#each priceData as item}
                        <option value={item.name}>{item.name}</option>
                    {/each}
                </select>
            </div>
            <div class="flex justify-center">
                <canvas id="priceChart" width="400" height="230"></canvas>
            </div>
        </div>

        <!-- Right column for groceries list -->
        <div class="w-1/4 p-4">
            <h2 class="text-xl mb-4">Groceries List</h2>
            <div class="flex items-center gap-2">
                <input type="checkbox" id="selectAll" />
                <label for="selectAll">Select All</label>
            </div>
            <div class="flex flex-col gap-2 overflow-auto" style="max-height: 650px;">
                {#each priceData as item}
                    <div class="w-[320px] space-y-2">
                        <div class="flex items-baseline gap-5 rounded-md border px-4 py-3 font-mono text-sm">
                            <input type="checkbox" value={item.name} checked={selectedGroceries.includes(item.name)} />
                            <div class="">{item.name}</div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>
