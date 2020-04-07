window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

const deleteBoxes_venue = document.querySelectorAll('.delete_item_venue');
for (let i = 0; i < deleteBoxes_venue.length; i++) {
    const delete_item = deleteBoxes_venue[i];
    delete_item.onclick = (e) => {
        const id = e.target.attributes['data_id'].value;
        fetch('/venues/' + id, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((response) => {
            location.href='/venues';
            console.log("deleted");
        });
    }
}

const deleteBoxes_artist = document.querySelectorAll('.delete_item_artist');
for (let i = 0; i < deleteBoxes_artist.length; i++) {
    const delete_item = deleteBoxes_artist[i];
    delete_item.onclick = (e) => {
        const id = e.target.attributes['data_id'].value;
        fetch('/artists/' + id, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((response) => {
            location.href='/artists';
            console.log('deleted');
        });
    }
}