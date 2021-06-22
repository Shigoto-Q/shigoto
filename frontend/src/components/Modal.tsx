import { Modal, Button } from "rsuite";

interface ModalProps {
  show: boolean;
  close: any;
}

const RepoModal = ({ show, close }: ModalProps) => {
  return (
    <Modal show={show} onHide={close}>
      <Modal.Header>
        <Modal.Title>Modal Title</Modal.Title>
      </Modal.Header>
      <Modal.Body>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={close(false)} appearance="primary">
          Ok
        </Button>
        <Button onClick={close(false)} appearance="subtle">
          Cancel
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default RepoModal
