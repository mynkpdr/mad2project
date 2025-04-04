import router from "../router";
import ConfirmationModal from "../components/modals/ConfirmationModal.vue";
import { createApp } from 'vue';
import { push } from "notivue";
import axios from "axios";
import { useNightModeStore } from "../store/nightMode";

export function dataTableDefaults(datatable, labels = {}, columns = []) {
    if (datatable.value) {
        // Destroy any existing DataTable instance to avoid re-initialization issues
        if (datatable.value.simpleDatatables) {
            datatable.value.simpleDatatables.destroy();
        }
        datatable.value.simpleDatatables = new simpleDatatables.DataTable(datatable.value, {
            perPage: parseInt(localStorage.getItem('adminItemsPerPage')) || 10,
            perPageSelect: [5, 10, 20, 50, 100],
            searchQuerySeparator: ",",
            labels: labels,
            columns: columns,
        });
    const {isNightMode} = useNightModeStore();
    isNightMode ? datatable.value.simpleDatatables.wrapperDOM.querySelector('.datatable-top .datatable-dropdown .datatable-selector').classList.add('night-mode') : null
    isNightMode ? datatable.value.simpleDatatables.wrapperDOM.querySelector('.datatable-top .datatable-search .datatable-input').classList.add('night-mode') :  null

        
        const rebindClickEvent = () => {
            // the action buttons are not reactive, so we need to rebind the click event
            datatable.value.querySelectorAll('.view-btn').forEach(button => {
                button.addEventListener('click', (event) => {
                    const action = event.currentTarget.dataset.action;
                    const id = event.currentTarget.dataset.id;
                    const take_quiz_id = event.currentTarget.dataset.take_quiz_id;
                    console.log(action, id, take_quiz_id)
                    if (action && id && take_quiz_id) {
                        router.push({ name: action, params: { id: id, take_quiz_id: take_quiz_id } });
                    } else if (action && id) {
                        router.push({ name: action, params: { id: id } });
                    }
                });
            });

            // the action buttons are not reactive, so we need to rebind the click event
            datatable.value.querySelectorAll('.edit-btn').forEach(button => {
                button.addEventListener('click', (event) => {
                    const action = event.currentTarget.dataset.action;
                    const id = event.currentTarget.dataset.id;
                    if (action && id) {
                        router.push({ name: action, params: { id: id }, query: { edit: true } });
                    }
                });
            });

            // the action buttons are not reactive, so we need to rebind the click event
            datatable.value.querySelectorAll('.delete-btn').forEach(button => {
                button.addEventListener('click', (event) => {
                    const confirmation_message = event.currentTarget.dataset.confirmation_message;
                    const success_message = event.currentTarget.dataset.success_message;
                    const delete_url = event.currentTarget.dataset.delete_url;
                    const id = event.currentTarget.dataset.id;
                    if (delete_url && id) {
                        const modalDiv = document.createElement('div');
                        document.body.appendChild(modalDiv);

                        const modalApp = createApp(ConfirmationModal, {
                            title: 'Delete Confirmation',
                            message: confirmation_message ? confirmation_message : 'Are you sure you want to delete this record?',
                            visible: true,
                            onClose: () => {
                                modalApp.unmount();
                                modalDiv.remove();
                            },
                            onConfirm: () => {
                                const handleConfirm = async () => {
                                    try {
                                        await axios.delete(delete_url);
                                        modalApp.unmount();
                                        modalDiv.remove();
                                        push.success(success_message ? success_message : 'Record deleted successfully');
                                        const currentRoute = router.currentRoute.value;
                                        router.replace('/reload-temp').then(() => {
                                            router.replace(currentRoute.fullPath);
                                        });
                                    } catch (error) {
                                        modalApp.unmount();
                                        modalDiv.remove();
                                        throw error;
                                    }
                                };
                                handleConfirm();
                            }
                        });

                        modalApp.mount(modalDiv);
                    }
                });
            });

            
            datatable.value.querySelectorAll('tbody tr').forEach(row => {
                row.addEventListener('click', (event) => {
                    // Check if the clicked element is a button or part of the action buttons
                    const clickedElement = event.target;
                    if (clickedElement.closest('.view-btn') || clickedElement.closest('.edit-btn') || clickedElement.closest('.delete-btn')) {
                        return; // Don't trigger the row click if an action button was clicked
                    }
                    const viewClick = event.currentTarget.closest('tr').lastElementChild.querySelector('.view-btn')
                    if (!viewClick) {
                        return; // Don't trigger the row click if there is no view button
                    }
                    const id = viewClick.dataset.id;
                    const action = viewClick.dataset.action;
                    const take_quiz_id = viewClick.dataset.take_quiz_id;
                    console.log(action, id, take_quiz_id)
                    if (action && id && take_quiz_id) {
                        router.push({ name: action, params: { id: id, take_quiz_id: take_quiz_id } });
                    } else if (action && id) {
                        router.push({ name: action, params: { id: id } });
                    } else {
                        push.error('No action found for this row');
                    }
                });
            });
            

        };

        // there will be a bug if we don't rebind the click event after the init and search update events
        datatable.value.simpleDatatables.on('datatable.init', rebindClickEvent);
        datatable.value.simpleDatatables.on('datatable.update', rebindClickEvent);
    }
}
