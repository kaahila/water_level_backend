const GRAPH_DATA_LIMIT = 100;


window.onload = (_) => {
    updateLevel();
    setInterval(updateLevel, 1000);
}

window.addEventListener("DOMContentLoaded", async function() {
    await renderChart();
}, false);

const renderChart = async () => {
    const ctx = document.getElementById('chart');
    const data = await fetch(`/items?limit=${GRAPH_DATA_LIMIT}`).then(r => r.json()).then(response => {
        return response.map(entry => {
            console.log(entry['created_on']);
            return {
                level: entry['value'],
                timestamp: entry['created_on'],
            }
        }).map((entry) => {
            const date = new Date(entry.timestamp);
            const dateFormat = date.toLocaleDateString("de-DE", {
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit"
            });
            return {level: entry.level, date: dateFormat}
        });
    });

    console.log(data);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map((entry) => entry.date),
            datasets: [{
                label: 'Wasserlevel',
                data: data.map((entry) => entry.level),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            interaction: {
            intersect: false,
            },
            scales: {
            x: {
                display: true,
                title: {
                display: true
                }
            },
            y: {
                display: true,
                title: {
                display: true,
                text: 'Wasserlevel'
                },
                suggestedMin: 0,
                suggestedMax: 6
            }
            }
        },
    });
}

const updateLevel = () => {
    const realContainerHeight = 9.46; // cm
    fetch(`/latestItem`).then(r => r.json()).then(response => {
        const realLevel = response['value'].toFixed(2);
        const virtualContainerHeight = document.getElementById('water-container').offsetHeight;
        const virtualLevel = (virtualContainerHeight / realContainerHeight) * realLevel;
        const realLevelInPercent = 100 / realContainerHeight * realLevel;


        if(virtualLevel > virtualContainerHeight) {
            document.getElementById('water-level').innerHTML = ``;
            document.getElementById('water-container-level').setAttribute("style",`height:${virtualContainerHeight}px`);
        } else {
            document.getElementById('water-level').innerHTML = `${realLevelInPercent.toFixed(2)}% - ${realLevel}cm`;
            document.getElementById('water-container-level').setAttribute("style",`height:${virtualLevel}px`);
        }
    });
}