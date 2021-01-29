import React from "react"
import {
    Container,
    Row,
    Col,
    Form,
    FormControl,
    ButtonGroup,
    ToggleButton,
    DropdownButton,
    Dropdown,
    InputGroup,
    Button
} from "react-bootstrap"
import {
    VictoryChart,
    VictoryLine,
    VictoryTheme,
    VictoryAxis
} from "victory"
import {MdEnhancedEncryption} from "react-icons/md"
import {GiHammerBreak} from "react-icons/gi"
import axios from "axios"
import "./stylesheets/App.css"

const actions = [
    {
        name: "Encrypt",
        value: "encrypt"
    },
    {
        name: "Decrypt",
        value: "decrypt"
    }
]

const strategies = [
    {
        name: "Bruteforce",
        value: "bruteforce"
    },
    {
        name: "Hill Climbing",
        value: "hill-climbing"
    }
]

class App extends React.Component{

    constructor(props){

        super(props)

        /* Initialize the state */
        this.state = {
            selected_action: "encrypt",
            encryption_details: {
                plaintext: "",
                cipher: "",
                key: "",
                ciphertext: ""
            },
            decryption_details: {
                strategy: "bruteforce",
                ciphertext: "",
                plaintext: "",
                heuristic_values: []
            }
        }

        /* Bind methods */
        this.changePlaintext = this.changePlaintext.bind(this)
        this.changeEncryptionKey = this.changeEncryptionKey.bind(this)
        this.selectCipher = this.selectCipher.bind(this)
        this.encryptText = this.encryptText.bind(this)
        this.changeCiphertext = this.changeCiphertext.bind(this)
        this.decryptText = this.decryptText.bind(this)

    }

    selectAction(event){

        var modified_state = this.state

        modified_state.selected_action = event.target.value
        this.setState(modified_state)

    }

    changePlaintext(event){

        var modified_state = this.state

        modified_state.encryption_details.plaintext = event.target.value
        this.setState(modified_state)

    }

    changeEncryptionKey(event){

        var modified_state = this.state

        modified_state.encryption_details.key = event.target.value
        this.setState(modified_state)

    }

    selectCipher(event){

        var modified_state = this.state

        modified_state.encryption_details.cipher = event
        this.setState(modified_state)

    }

    async encryptText(){

        axios.get("http://127.0.0.1:3001/encrypt", {
            headers: {
                "Access-Control-Allow-Origin": "*"
            },
            params: {
                plaintext: this.state.encryption_details.plaintext,
                cipher: this.state.encryption_details.cipher,
                key: this.state.encryption_details.key
            }
        }).then(response => {

            var modified_state = this.state

            modified_state.encryption_details.ciphertext = response.data.ciphertext
            this.setState(modified_state)

        }).catch(error => console.log(error));

    }

    changeCiphertext(event){

        var modified_state = this.state

        modified_state.decryption_details.ciphertext = event.target.value
        this.setState(modified_state)

    }

    selectStrategy(event){

        var modified_state  = this.state

        modified_state.decryption_details.strategy = event.target.value
        this.setState(modified_state)

    }

    decryptText(){

        axios.get("http://127.0.0.1:3001/decrypt", {
            headers: {
                "Access-Control-Allow-Origin": "*"
            },
            params: {
                ciphertext: this.state.decryption_details.ciphertext,
                strategy: this.state.decryption_details.strategy
            }
        }).then(response => {

            var modified_state = this.state

            modified_state.decryption_details.plaintext = response.data.plaintext
            modified_state.decryption_details.heuristic_values = response.data.heuristic_values
            this.setState(modified_state)

        }).catch(error => console.log(error));

    }

    render(){

        var area_classes = "area"
        var cipher_button_label = "Cipher"
        var encrypt_container_classes = "encryption-container"
        var decrypt_container_classes = "decryption-container"
        var selected_cipher

        // Get specific classes and labels
        if (this.state.selected_action === "encrypt"){

            encrypt_container_classes += " show"

            selected_cipher = this.state.encryption_details.cipher
            if (selected_cipher !== "")
                cipher_button_label = selected_cipher.replace(/^\w/, (c) => c.toUpperCase())

        }
        else{
            area_classes += " decrypt"
            decrypt_container_classes += " show"
        }

        return (
            <div className="App">

                <div className="context">

                    {/* Logo and application name */}
                    <img src="images/logo.png" alt="Naevia Logo"></img>
                    <h1>Naevia</h1>

                    {/* Action buttons */}
                    <ButtonGroup toggle>
                        {actions.map((action, idx) => (
                            <ToggleButton
                                key={idx}
                                type="radio"
                                name="radio"
                                className="action-select"
                                value={action.value}
                                checked={this.state.selected_action === action.value}
                                onClick={(e) => this.selectAction(e)}
                            >
                                {action.name}
                            </ToggleButton>
                        ))}
                    </ButtonGroup>

                    {/* Encryption container */}
                    <Container fluid="md" className={encrypt_container_classes}>

                        {/* Plaintext */}
                        <Form.Control
                            as="textarea"
                            placeholder="Plaintext"
                            value={this.state.encryption_details.plaintext}
                            onChange={this.changePlaintext}
                        />

                        {/* Options */}
                        <InputGroup className="mb-3 options-group">

                            <FormControl
                                className="key-chooser"
                                aria-describedby="basic-addon1"
                                placeholder="Encryption Key"
                                value={this.state.encryption_details.key}
                                onChange={this.changeEncryptionKey}
                            />

                            <DropdownButton
                                as={InputGroup.Append}
                                title={cipher_button_label}
                                drop="right"
                                variant="light"
                                className="cipher-chooser"
                                onSelect={this.selectCipher}
                            >
                                <Dropdown.Item eventKey="caesar">Caesar</Dropdown.Item>
                                <Dropdown.Item eventKey="vigenere">Vigenere</Dropdown.Item>
                                <Dropdown.Item eventKey="substitution">Substitution</Dropdown.Item>
                            </DropdownButton>

                        </InputGroup>

                        {/* Button */}
                        <Button
                            block
                            variant="light"
                            className="encrypt-button"
                            onClick={this.encryptText}
                        >
                            <MdEnhancedEncryption/>
                        </Button>

                        {/* Ciphertext */}
                        <Form.Control
                            as="textarea"
                            disabled
                            placeholder="Produced ciphertext"
                            value={this.state.encryption_details.ciphertext}
                        />

                    </Container>

                    {/* Decryption container */}
                    <Container fluid="md" className={decrypt_container_classes}>

                        {/* Ciphertext */}
                        <Form.Control
                            as="textarea"
                            placeholder="Ciphertext"
                            value={this.state.decryption_details.ciphertext}
                            onChange={this.changeCiphertext}
                        />

                        {/* Strategy */}
                        <ButtonGroup toggle>
                            {strategies.map((strategy, idx) => (
                                <ToggleButton
                                    key={idx}
                                    type="radio"
                                    name="radio"
                                    className="strategy-select"
                                    value={strategy.value}
                                    checked={this.state.decryption_details.strategy === strategy.value}
                                    onClick={(e) => this.selectStrategy(e)}
                                >
                                    {strategy.name}
                                </ToggleButton>
                            ))}
                        </ButtonGroup>

                        {/* Button */}
                        <Button
                            block
                            variant="light"
                            className="decrypt-button"
                            onClick={this.decryptText}
                        >
                            <GiHammerBreak/>
                        </Button>

                        <Row>

                            {/* Plaintext */}
                            <Col className="plaintext-container">
                                <Form.Control
                                    as="textarea"
                                    disabled
                                    placeholder="Produced plaintext"
                                    value={this.state.decryption_details.plaintext}
                                />
                            </Col>

                            {/* Heuristic value */}
                            <Col className="heuristic-plot">
                                <VictoryChart theme={VictoryTheme.grayscale}>

                                    <VictoryAxis 
                                        label="Iterations"
                                        tickFormat={() => ""}
                                    />
                                    <VictoryAxis
                                        dependentAxis
                                        label="Heuristic Values"
                                        tickFormat={() => ""}
                                    />

                                    <VictoryLine
                                        data={this.state.decryption_details.heuristic_values}
                                        interpolation="natural"
                                    />

                                </VictoryChart>
                            </Col>

                        </Row>

                    </Container>

                </div>

                {/* Background animation */}
                <div className={area_classes}>
                    <ul className="circles">
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                        <li></li>
                    </ul>
                </div>

            </div>
        )
    }
}

export default App