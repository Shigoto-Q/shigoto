import { Component } from "react";
import { Checkbox, CheckboxGroup, Button, Modal, ButtonToolbar } from "rsuite";
import api from "../../api/";
import "rsuite/dist/styles/rsuite-default.css";

interface RepoProps {
  optionsProps: any;
}

class SelectRepo extends Component<RepoProps, any> {
  constructor(props: any) {
    super(props);
    this.state = {
      indeterminate: true,
      checkAll: false,
      options: [],
      loading: true,
      show: false,
    };
    this.handleCheckAll = this.handleCheckAll.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.submitRepos = this.submitRepos.bind(this);
    this.closeModal = this.closeModal.bind(this);
    this.openModal = this.openModal.bind(this);
    this.findRepo = this.findRepo.bind(this);
  }
  closeModal() {
    this.setState({ show: false });
  }
  openModal() {
    this.setState({ show: true });
  }
  handleCheckAll(value: any, checked: any) {
    const nextValue = checked ? this.state.options : [];
    this.setState({
      value: nextValue,
      indeterminate: false,
      checkAll: checked,
    });
  }
  handleChange(value: any) {
    this.setState({
      value,
      indeterminate:
        value.length > 0 && value.length < this.state.options.length,
      checkAll: value.length === this.state.options.length,
    });
  }

  findRepo(repo: any, name: string) {
    return repo.full_name === name;
  }
  submitRepos() {
    var repos = this.props.optionsProps
      .filter((repo: any) => this.state.value.includes(repo.full_name))
      .map((v: any) => ({ full_name: v.full_name, repo_url: v.clone_url, language: v.language }));
    console.log(repos)
    api.post("/api/v1/github/repository/", repos)
    this.setState({ show: false });
  }

  componentDidMount() {
    if (this.props.optionsProps) {
      const arr = this.props.optionsProps.map((a: any) => {
        return a.full_name;
      });
      this.setState({ options: [...this.state.options, ...arr] });
    }
    this.setState({ loading: false });
  }

  render() {
    if (!this.state.loading) {
      return (
        <div>
          <ButtonToolbar>
            <button
              type="submit"
              onClick={this.openModal}
              className="inline-flex 
                           justify-center 
                           py-2 px-4 
                           border border-transparent 
                           shadow-sm text-sm 
                           font-medium 
                           rounded-md 
                           text-white 
                           bg-indigo-600 
                           hover:bg-indigo-700 
                           focus:outline-none 
                           focus:ring-2 
                           focus:ring-offset-2 
                           focus:ring-indigo-500"
            >
              Select repositories
            </button>
          </ButtonToolbar>
          <Modal size="xs" show={this.state.show} onHide={this.closeModal}>
            <Modal.Header>
              <Modal.Title>GitHub Repositories</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Checkbox
                indeterminate={this.state.indeterminate}
                checked={this.state.checkAll}
                onChange={this.handleCheckAll}
              >
                Check all
              </Checkbox>
              <hr />
              <CheckboxGroup
                name="checkboxList"
                value={this.state.value}
                onChange={this.handleChange}
              >
                {this.state.options.map((a: any, idx: any) => {
                  return (
                    <Checkbox value={a} key={idx}>
                      {a}
                    </Checkbox>
                  );
                })}
              </CheckboxGroup>
            </Modal.Body>
            <Modal.Footer>
              <Button onClick={this.submitRepos} appearance="primary">
                Ok
              </Button>
              <Button onClick={this.closeModal} appearance="subtle">
                Cancel
              </Button>
            </Modal.Footer>
          </Modal>
        </div>
      );
    } else {
      return <div>Bruh</div>;
    }
  }
}

export default SelectRepo;
