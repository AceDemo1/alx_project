function deleteEmission(emission_id) {
    fetch('/delete-emission', {
        method: 'POST',
        body: JSON.stringify({ emission_id: emission_id })
    }).then((_res) => {
        window.location.href = "/carbon-history";
    });
}