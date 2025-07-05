document.addEventListener('DOMContentLoaded', function() {
    // Track the highest ID used so far to ensure unique IDs
    let highestId = 1;

    // Initialize event listeners for existing elements
    initializeEventListeners();

    function initializeEventListeners() {
        // Add event listener for add buttons
        document.querySelectorAll('.button--add').forEach(button => {
            button.addEventListener('click', addNewTodoItem);
        });

        // Add event listener for remove buttons
        document.querySelectorAll('.button--remove').forEach(button => {
            button.addEventListener('click', removeTodoItem);
        });

        // Update the highest ID based on existing items
        document.querySelectorAll('.todo__item').forEach(item => {
            const itemId = parseInt(item.id);
            if (itemId > highestId) {
                highestId = itemId;
            }
        });
    }

    function addNewTodoItem(event) {
        // Get the parent todo item
        const currentItem = event.currentTarget.closest('.todo__item');
        
        // Create a new ID for the new item
        highestId++;
        const newId = highestId;
        
        // Clone the current item
        const newItem = currentItem.cloneNode(true);
        
        // Update the ID and data attributes
        newItem.id = newId;
        newItem.querySelectorAll('[data-id]').forEach(element => {
            element.setAttribute('data-id', newId);
        });
        
        // Clear input values in the new item
        newItem.querySelector('input[type="text"]').value = '';
        newItem.querySelector('select').selectedIndex = 0;
        newItem.querySelector('input[type="checkbox"]').checked = false;
        
        // Update checkbox ID and label 'for' attribute
        const checkbox = newItem.querySelector('input[type="checkbox"]');
        checkbox.id = `checkboxInput${newId}`;
        checkbox.name = `todo_check[${newId}]`;
        newItem.querySelector('label').setAttribute('for', `checkboxInput${newId}`);
        
        // Add event listeners to the new item's buttons
        newItem.querySelector('.button--add').addEventListener('click', addNewTodoItem);
        newItem.querySelector('.button--remove').addEventListener('click', removeTodoItem);
        
        // Insert the new item after the current one
        currentItem.after(newItem);
    }

    function removeTodoItem(event) {
        const todoItems = document.querySelectorAll('.todo__item');
        
        // Only remove if there's more than one item
        if (todoItems.length > 1) {
            event.currentTarget.closest('.todo__item').remove();
        } else {
            // If it's the last item, just clear its values
            const item = event.currentTarget.closest('.todo__item');
            item.querySelector('input[type="text"]').value = '';
            item.querySelector('select').selectedIndex = 0;
            item.querySelector('input[type="checkbox"]').checked = false;
        }
    }

    // Optional: Add functionality to save todos in local storage
    function saveTodos() {
        const todoItems = document.querySelectorAll('.todo__item');
        const todos = [];
        
        todoItems.forEach(item => {
            todos.push({
                id: item.id,
                text: item.querySelector('input[type="text"]').value,
                optionValue: item.querySelector('select').value,
                checked: item.querySelector('input[type="checkbox"]').checked
            });
        });
        
        localStorage.setItem('todos', JSON.stringify(todos));
    }

    // Optional: Load todos from local storage
    function loadTodos() {
        const savedTodos = localStorage.getItem('todos');
        
        if (savedTodos) {
            const todos = JSON.parse(savedTodos);
            const todoItemsContainer = document.querySelector('.todo__items');
            const templateItem = document.querySelector('.todo__item');
            
            // Clear existing items except the first one (template)
            todoItemsContainer.innerHTML = '';
            todoItemsContainer.appendChild(templateItem);
            
            todos.forEach((todo, index) => {
                if (index === 0) {
                    // Update the template item with first saved todo
                    templateItem.id = todo.id;
                    templateItem.querySelector('input[type="text"]').value = todo.text;
                    templateItem.querySelector('select').value = todo.optionValue;
                    templateItem.querySelector('input[type="checkbox"]').checked = todo.checked;
                } else {
                    // Create new items for remaining todos
                    const newItem = templateItem.cloneNode(true);
                    newItem.id = todo.id;
                    newItem.querySelector('input[type="text"]').value = todo.text;
                    newItem.querySelector('select').value = todo.optionValue;
                    newItem.querySelector('input[type="checkbox"]').checked = todo.checked;
                    
                    // Update checkbox ID and label
                    const checkbox = newItem.querySelector('input[type="checkbox"]');
                    checkbox.id = `checkboxInput${todo.id}`;
                    newItem.querySelector('label').setAttribute('for', `checkboxInput${todo.id}`);
                    
                    todoItemsContainer.appendChild(newItem);
                }
                
                // Update highest ID
                if (parseInt(todo.id) > highestId) {
                    highestId = parseInt(todo.id);
                }
            });
            
            // Re-initialize event listeners
            initializeEventListeners();
        }
    }

    // Uncomment these lines to enable local storage functionality
    loadTodos();
    
    // Add event listeners to inputs to save todos when changed
    document.querySelector('.todo__items').addEventListener('change', saveTodos);
    document.querySelector('.todo__items').addEventListener('input', saveTodos);
});