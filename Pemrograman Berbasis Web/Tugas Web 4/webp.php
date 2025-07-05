<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $texts = $_POST['todo_text'] ?? [];
    $options = $_POST['todo_option'] ?? [];
    $checkboxes = $_POST['todo_check'] ?? [];

    echo "<h2>Submitted Todo Items:</h2>";
    echo "<ul>";
    if ((empty(array_filter($texts)))){
            echo "No data submitted.";
        }
    for ($i = 0; $i < count($texts); $i++) {
        if ($texts[$i] != null){
            $text = htmlspecialchars($texts[$i]);
            $option = htmlspecialchars($options[$i]);
            $isChecked = isset($_POST['todo_check'][$i]) ? 'Yes' : 'No';
            echo "<li>";
            echo "Text: $text<br>";
            echo "Option: $option<br>";
            echo "Checked: $isChecked<br>";
            echo "</li><br>";
        }
    }
    echo "</ul>";
} else {
    echo "No data submitted.";
}
?>
