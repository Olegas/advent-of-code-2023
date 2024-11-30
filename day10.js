const s = 5;
const h = 2;


const movements = {
    '|': {
        '0,1': [0, 1],
        '0,-1': [0, -1]
    },
    '-': {
        '1,0': [1, 0],
        '-1,0': [-1, 0]
    },
    'L': {
        '-1,0': [0, -1],
        '0,1': [1, 0]
    },
    'F': {
        '0,-1': [1, 0],
        '-1,0': [0, 1]
    },
    'J': {
        '1,0': [0, -1],
        '0,1': [-1, 0]
    },
    '7': {
        '1,0': [0, 1],
        '0,-1': [-1, 0]
    }
}

const pos_to_right = {
    '|': {
        '0,1': [[-1, 0]],
        '0,-1': [[1, 0]]
    },
    '-': {
        '1,0': [[0, 1]],
        '-1,0': [[0, -1]]
    },
    'L': {
        '-1,0': [],
        '0,1': [[-1, 0], [0, 1]]
    },
    'F': {
        '0,-1': [],
        '-1,0': [[0, -1], [-1, 0]]
    },
    'J': {
        '1,0': [[1, 0], [0, 1]],
        '0,1': []
    },
    '7': {
        '1,0': [],
        '0,-1': [[1, 0], [0, -1]]
    }
}

function check_right(cur_dir, cur_pos, seen, limits, all_grid, ctx) {
    const [x, y] = cur_pos.split(',').map(Number)
    const c = all_grid[cur_pos]
    const deltas = pos_to_right[c][cur_dir]
    for (let d of deltas) {
        const [dx, dy] = d
        const np = [x + dx, y + dy]
        const nps = np.join(',')
        if (!seen.has(nps) && !limits.has(nps)) {
            wave(nps, seen, limits, ctx)
        }
    }
}


function wave(wave_pos, seen, limits, ctx) {
    const to_check = [wave_pos]
    while (to_check.length > 0) {
        const i = to_check.pop()
        const [x, y] = i.split(',').map(Number);
        for (let a of around) {
            const [dx, dy] = a;
            const np = [x + dx, y + dy]
            const nps = np.join(',')
            if (!seen.has(nps) && !limits.has(nps)) {
                if (!limits.has(nps)) {
                    seen.add(nps);
                    requestAnimationFrame(() => {
                        ctx.beginPath();
                        ctx.rect(np[0] * s, np[1] * s, s, s);
                        ctx.fill();
                    })
                }
                to_check.push(nps)
            }
        }
    }
}

const around = [[-1, 0], [1, 0], [0, 1], [0, -1], [0, 0]]

function drawFig(sym, x, y, ctx) {

    switch (sym) {
        case '|':
            ctx.moveTo(x * s + h, y * s);
            ctx.lineTo(x * s + h, (y + 1) * s);
            break;
        case '-':
            ctx.moveTo(x * s, y * s + h);
            ctx.lineTo((x + 1) * s, y * s + h);
            break
        case 'F':
            ctx.moveTo(x * s + h, (y + 1) * s);
            ctx.lineTo(x * s + h, y * s + h);
            ctx.lineTo((x + 1) * s, y * s + h);
            break
        case 'L':
            ctx.moveTo(x * s + h, y * s);
            ctx.lineTo(x * s + h, y * s + h);
            ctx.lineTo((x + 1) * s, y * s + h);
            break
        case '7':
            ctx.moveTo(x * s, y * s + h);
            ctx.lineTo(x * s + h, y * s + h);
            ctx.lineTo(x * s + h, (y + 1) * s);
            break;
        case 'J':
            ctx.moveTo(x * s + h, y * s);
            ctx.lineTo(x * s + h, y * s + h);
            ctx.lineTo(x * s, y * s + h);
    }
}

fetch('./js.json').then(r => r.json()).then(({
                                                 max_x, max_y, path, map, start, start_sym, start_direction
                                             }) => {
    const canvas = document.getElementById('cnv');
    const ctx = canvas.getContext('2d');
    const pathSet = new Set(path)
    ctx.beginPath()
    ctx.fillStyle = 'blue';
    ctx.strokeStyle = 'red';

    for (let y = 0; y <= max_y; y++) {
        for (let x = 0; x <= max_x; x++) {
            const pos = `${x},${y}`
            if (pathSet.has(pos)) {
                const sym = map[pos]
                drawFig(sym, x, y, ctx)
            }
        }
    }
    ctx.stroke()

    let direction = start_direction.join(',')
    const start_pos = start.join(',')
    map[start_pos] = start_sym
    let pos = start_pos;
    const seen = new Set()
    ctx.strokeStyle = 'blue';
    const seenCtr = document.getElementById('seen');
    function step() {
        check_right(direction, pos, seen, pathSet, map, ctx)
        const pipe = map[pos]
        const m = movements[pipe]
        direction = m[direction]
        const [dx, dy] = direction
        const [x, y] = pos.split(',').map(Number);
        ctx.beginPath()
        drawFig(pipe, x, y, ctx);
        ctx.stroke();
        pos = [x + dx, y + dy].join(',')
        seenCtr.innerText = `Seen: ${seen.size}`;
        if (pos !== start_pos) requestAnimationFrame(step)
        else alert(seen.size);
    }
    requestAnimationFrame(step);

})
