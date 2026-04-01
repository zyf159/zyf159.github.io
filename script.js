// 数据可视化
window.onload = function() {
    // 政策数据
    const policyData = [
        {
            "city": "平顶山",
            "isIndustry": true,
            "title": "平顶山市人民政府关于做好2025年烟花爆竹禁放限放有关工作的通告",
            "url": "https://www.pds.gov.cn/contents/31700/425211.html",
            "release_date": "2024-12-17",
            "file_number": "通告〔2024〕3号",
            "category": "政府通告",
            "publisher": "",
            "written_date": "",
            "content": "..."
        },
        {
            "city": "平顶山",
            "isIndustry": true,
            "title": "平顶山市人民政府关于调整高排放非道路移动机械禁用区域的通告",
            "url": "https://www.pds.gov.cn/contents/31700/411597.html",
            "release_date": "2024-08-26",
            "file_number": "通告〔2024〕2号",
            "category": "政府通告",
            "publisher": "",
            "written_date": "",
            "content": "..."
        },
        {
            "city": "平顶山",
            "isIndustry": true,
            "title": "平顶山市人民政府关于加强2024年春节期间烟花爆竹安全管理的通告",
            "url": "https://www.pds.gov.cn/contents/31700/400069.html",
            "release_date": "2024-01-30",
            "file_number": "通告〔2024〕1号",
            "category": "政府通告",
            "publisher": "",
            "written_date": "",
            "content": "..."
        },
        {
            "city": "平顶山",
            "isIndustry": true,
            "title": "平顶山市人民政府关于2023年春节期间烟花爆竹燃放的通告",
            "url": "https://www.pds.gov.cn/contents/31700/355823.html",
            "release_date": "2023-01-19",
            "file_number": "通告〔2023〕1号",
            "category": "政府通告",
            "publisher": "",
            "written_date": "",
            "content": "..."
        }
    ];

    // 生成政策发布年份数据
    const years = {};
    policyData.forEach(policy => {
        const year = policy.release_date.split('-')[0];
        if (years[year]) {
            years[year]++;
        } else {
            years[year] = 1;
        }
    });

    // 准备图表数据
    const labels = Object.keys(years).sort();
    const data = labels.map(label => years[label]);

    // 创建图表
    const ctx = document.getElementById('policyChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '政策发布数量',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: '政策发布年份分布',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                }
            }
        }
    });

    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // 导航栏滚动效果
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.backgroundColor = 'rgba(51, 51, 51, 0.95)';
        } else {
            navbar.style.backgroundColor = '#333';
        }
    });

    // 项目卡片悬停效果
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
};
