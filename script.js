    class SkipListNode {
            constructor(value, level) {
                this.value = value;
                this.forward = new Array(level + 1).fill(null);
                this.level = level;
            }
        }

        class SkipList {
            constructor() {
                this.maxLevel = 15;
                this.probability = 0.5;
                this.level = 0;
                this.header = new SkipListNode(-Infinity, this.maxLevel);
                this.nil = new SkipListNode(Infinity, this.maxLevel);
                
                // Initialize header forward pointers to nil
                for (let i = 0; i <= this.maxLevel; i++) {
                    this.header.forward[i] = this.nil;
                }
            }

            randomLevel() {
                let level = 0;
                while (Math.random() < this.probability && level < this.maxLevel) {
                    level++;
                }
                return level;
            }

            search(value) {
                let current = this.header;
                let searchPath = [];
                let level;

                for (let i = this.level; i >= 0; i--) {
                    while (current.forward[i].value < value) {
                        searchPath.push({level: i, node: current});
                        current = current.forward[i];
                    }
                    searchPath.push({level: i, node: current});

                    level = i; // Store the last level checked
                    if (current.forward[i].value == value) break;
                }
                
                current = current.forward[level];
                const found = current.value === value;
                return {found, node: found ? current : null, searchPath};
            }

            insert(value) {
                let update = new Array(this.maxLevel + 1);
                let current = this.header;

                // Find update array
                for (let i = this.level; i >= 0; i--) {
                    while (current.forward[i].value < value) {
                        current = current.forward[i];
                    }
                    update[i] = current;
                }

                current = current.forward[0];

                // If value already exists, don't insert
                if (current.value === value) {
                    return false;
                }

                // Generate random level
                let newLevel = this.randomLevel();

                // If new level is greater than current level, update header
                if (newLevel > this.level) {
                    for (let i = this.level + 1; i <= newLevel; i++) {
                        update[i] = this.header;
                    }
                    this.level = newLevel;
                }

                // Create new node
                let newNode = new SkipListNode(value, newLevel);

                // Update forward pointers
                for (let i = 0; i <= newLevel; i++) {
                    newNode.forward[i] = update[i].forward[i];
                    update[i].forward[i] = newNode;
                }

                return true;
            }

            delete(value) {
                let update = new Array(this.maxLevel + 1);
                let current = this.header;

                // Find update array
                for (let i = this.level; i >= 0; i--) {
                    while (current.forward[i].value < value) {
                        current = current.forward[i];
                    }
                    update[i] = current;
                }

                current = current.forward[0];

                // If value exists, delete it
                if (current.value === value) {
                    for (let i = 0; i <= this.level; i++) {
                        if (update[i].forward[i] !== current) break;
                        update[i].forward[i] = current.forward[i];
                    }

                    // Update level
                    while (this.level > 0 && this.header.forward[this.level].value === Infinity) {
                        this.level--;
                    }
                    return true;
                }
                return false;
            }

            getAllNodes() {
                let nodes = [];
                let current = this.header.forward[0];
                while (current.value !== Infinity) {
                    nodes.push(current);
                    current = current.forward[0];
                }
                return nodes;
            }

            clear() {
                this.level = 0;
                for (let i = 0; i <= this.maxLevel; i++) {
                    this.header.forward[i] = this.nil;
                }
            }
        }

        let skipList = new SkipList();
        let animationTimeout = null;

        function render(highlightPath = null, foundNode = null) {
            const container = document.getElementById('skiplistContainer');
            container.innerHTML = '';

            for (let level = skipList.level; level >= 0; level--) {
                const levelDiv = document.createElement('div');
                levelDiv.className = 'level';
                
                const labelDiv = document.createElement('div');
                labelDiv.className = 'level-label';
                labelDiv.textContent = `Level ${level}:`;
                levelDiv.appendChild(labelDiv);

                let current = skipList.header;
                while (current) {
                    const nodeDiv = document.createElement('div');
                    nodeDiv.className = 'node';
                    
                    if (current === skipList.header) {
                        nodeDiv.className += ' header';
                        nodeDiv.textContent = 'HEAD';
                    } else if (current === skipList.nil) {
                        nodeDiv.className += ' nil';
                        nodeDiv.textContent = 'NIL';
                    } else {
                        nodeDiv.textContent = current.value;
                    }

                    // Highlight search path
                    if (highlightPath && highlightPath.some(p => p.level === level && p.node === current)) {
                        nodeDiv.className += ' searching';
                    }

                    // Highlight found node
                    if (foundNode && current === foundNode && level <= foundNode.level) {
                        nodeDiv.className += ' found';
                    }

                    levelDiv.appendChild(nodeDiv);

                    if (current.forward[level]) {
                        const arrowDiv = document.createElement('span');
                        arrowDiv.className = 'arrow';
                        arrowDiv.textContent = '→';
                        levelDiv.appendChild(arrowDiv);
                    }

                    current = current.forward[level];
                }

                container.appendChild(levelDiv);
            }

            updateStats();
        }

        function updateStats() {
            const nodes = skipList.getAllNodes();
            document.getElementById('nodeCount').textContent = nodes.length;
            document.getElementById('maxLevel').textContent = skipList.level;
        }

        function log(message) {
            const logDiv = document.getElementById('operationsLog');
            const timestamp = new Date().toLocaleTimeString();
            logDiv.innerHTML += `[${timestamp}] ${message}\n`;
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        function insert() {
            const value = parseInt(document.getElementById('insertValue').value);
            if (isNaN(value)) return;

            const success = skipList.insert(value);
            if (success) {
                document.getElementById('lastOperation').textContent = `Insert ${value}`;
                log(`Inserted ${value} successfully`);
            } else {
                log(`Value ${value} already exists`);
            }
            
            render();
            document.getElementById('insertValue').value = '';
        }

        function search() {
            const value = parseInt(document.getElementById('searchValue').value);
            if (isNaN(value)) return;

            const result = skipList.search(value);
            document.getElementById('lastOperation').textContent = `Search ${value}`;
            document.getElementById('searchSteps').textContent = result.searchPath.length;

            if (result.found) {
                log(`Found ${value} in ${result.searchPath.length} steps`);
            } else {
                log(`${value} not found (${result.searchPath.length} steps)`);
            }

            // Animate search
            render(result.searchPath, result.node);
            
            document.getElementById('searchValue').value = '';
        }

        function remove() {
            const value = parseInt(document.getElementById('deleteValue').value);
            if (isNaN(value)) return;

            const success = skipList.delete(value);
            if (success) {
                document.getElementById('lastOperation').textContent = `Delete ${value}`;
                log(`Deleted ${value} successfully`);
            } else {
                log(`Value ${value} not found for deletion`);
            }
            
            render();
            document.getElementById('deleteValue').value = '';
        }

        function generateRandom() {
            const value = Math.floor(Math.random() * 100) + 1;
            skipList.insert(value);
            document.getElementById('lastOperation').textContent = `Random Insert ${value}`;
            log(`Randomly inserted ${value}`);
            render();
        }

        function clear() {
            skipList.clear();
            document.getElementById('lastOperation').textContent = 'Clear All';
            document.getElementById('searchSteps').textContent = '-';
            log('Cleared all nodes');
            render();
        }

        function toggleInfo() {
            const infoPanel = document.getElementById('infoPanel');
            infoPanel.classList.toggle('show');
        }

        // Initialize with some sample data
        [15, 25, 35, 45, 55].forEach(value => {
            skipList.insert(value);
        });

        render();
        log('Skip list initialized with sample data: 15, 25, 35, 45, 55');
    