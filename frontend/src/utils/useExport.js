import { ref } from 'vue';
import { push } from 'notivue';
import axios from 'axios';

export function useExport(datatable) {
    const isCSVModalVisible = ref(false);
    const isJSONModalVisible = ref(false);
    const CSVModalMessage = ref('');
    const JSONModalMessage = ref('');

    const openCSVModal = () => {
        if (localStorage.getItem('exportMethod') === 'email' || localStorage.getItem('adminExportMethod') === 'email') {
            CSVModalMessage.value = 'Confirm export to CSV? The file will be sent to your email.';
        } else {
            CSVModalMessage.value = 'Confirm export to CSV? The file will be downloaded directly.';
        }
        isCSVModalVisible.value = true;
    };

    const closeCSVModal = () => {
        isCSVModalVisible.value = false;
    };

    const openJSONModal = () => {
        if (localStorage.getItem('exportMethod') === 'email' || localStorage.getItem('adminExportMethod') === 'email') {
            JSONModalMessage.value = 'Confirm export to JSON? The file will be sent to your email.';
        } else {
            JSONModalMessage.value = 'Confirm export to JSON? The file will be downloaded directly.';
        }
        isJSONModalVisible.value = true;
    };

    const closeJSONModal = () => {
        isJSONModalVisible.value = false;
    };

    const handleCSVConfirm = async () => {
        if (datatable.value) {
            const exportMethod = localStorage.getItem('exportMethod') || localStorage.getItem('adminExportMethod') || 'direct';

            if (exportMethod === 'direct') {
                simpleDatatables.exportCSV(datatable.value.simpleDatatables, {
                    filename: datatable.value.simpleDatatables.containerDOM.baseURI.split('/').pop() + "_table",
                    lineDelimiter: "\n",
                    columnDelimiter: ",",
                });
                push.success('CSV export successful!');
            } else {
                try {
                    const csvData = simpleDatatables.exportCSV(datatable.value.simpleDatatables, {
                        download: false,
                        lineDelimiter: "\n",
                        columnDelimiter: ",",
                    });
                    await axios.post('/api/export/email', {
                        data: csvData,
                        type: 'csv'
                    });
                    push.success('CSV sent to your email!');
                } catch (error) {
                    push.error('Failed to send CSV to email');
                }
            }
        } else {
            push.error('DataTable instance is not initialized.');
        }
        closeCSVModal();
    };

    const handleJSONConfirm = async () => {
        if (datatable.value) {
            const exportMethod = localStorage.getItem('exportMethod') || localStorage.getItem('adminExportMethod') || 'direct';

            if (exportMethod === 'direct') {
                simpleDatatables.exportJSON(datatable.value.simpleDatatables, {
                    filename: datatable.value.simpleDatatables.containerDOM.baseURI.split('/').pop() + "_table",
                    replacer: null,
                    space: 2,
                });
                push.success('JSON export successful!');
            } else {
                try {
                    const jsonData = simpleDatatables.exportJSON(datatable.value.simpleDatatables, {
                        download: false,
                        replacer: null,
                        space: 2,
                    });
                    await axios.post('/api/export/email', {
                        data: jsonData,
                        type: 'json'
                    });
                    push.success('JSON sent to your email!');
                } catch (error) {
                    push.error('Failed to send JSON to email');
                }
            }
        } else {
            push.error('DataTable instance is not initialized.');
        }
        closeJSONModal();
    };

    return {
        isCSVModalVisible,
        isJSONModalVisible,
        CSVModalMessage,
        JSONModalMessage,
        openCSVModal,
        closeCSVModal,
        openJSONModal,
        closeJSONModal,
        handleCSVConfirm,
        handleJSONConfirm,
    };
}
