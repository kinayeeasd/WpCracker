# WpCracker - WordPress Login Cracker & Checker

![Banner](https://github.com/HackfutSec/WpCracker/blob/main/assets/banner.png)  
*A powerful tool for validating and cracking WordPress login credentials.*

---

## 📝 Description

**WpCracker** is a versatile tool designed to validate and crack WordPress login credentials. It supports multiple input formats and allows silent password testing. Results are categorized into separate files for easy analysis.

---

## ✨ Features

- **Credential Validation**: Checks username and password combinations on WordPress sites.
- **Silent Cracking**: Tests a password list to find valid credentials.
- **Multithreading**: Uses multiple threads to speed up the verification process.
- **Supported Formats**:
  - `host|user|pass`
  - `host;user;pass`
  - `host:user:pass`
  - `host user pass` (space-separated)
  - `host#username@password`
  - `http://host#username@password`
  - `https://host#username@password`
- **Organized Results**: Valid credentials are saved in `Good_WP.txt`, and failed attempts in `Bad_WP.txt`.

---

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HackfutSec/WpCracker.git
   cd WpCracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python WpCracker.py
   ```

---

## 🛠 Usage

1. Run the script:
   ```bash
   python WpCracker.py
   ```

2. Choose the format of your credential list (e.g., `host|user|pass`).

3. Enter the path to the file containing the credentials.

4. If a login fails, you can provide a password list to test.

5. Results will be saved in:
   - `Good_WP.txt`: Valid credentials.
   - `Bad_WP.txt`: Failed login attempts.

---

## 📂 Project Structure

```
WpCracker/
├── WpCracker.py          # Main script
├── requirements.txt      # Python dependencies
├── Good_WP.txt           # File for valid credentials
├── Bad_WP.txt            # File for failed attempts
├── assets/               # Folder for images (banner, etc.)
└── README.md             # Documentation
```

---

## 📜 Example Input File

### Format `host|user|pass`
```
example.com|admin|password123
example.com|user|password456
```

### Format `host#username@password`
```
example.com#admin@password123
http://example.com#admin@password456
https://example.com#admin@password789
```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributions

Contributions are welcome! If you'd like to improve this project, follow these steps:

1. Fork the project.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📧 Contact

If you have questions or suggestions, feel free to reach out:

- **Email**: [hackfut404](mailto:hackfut404@proton.com)
- **GitHub**: [HackfutSec](https://github.com/HackfutSec)
- **Telegram**: [@Hackfut](https://t.me/H4ckfutSec)

---

## 🌟 Acknowledgments

Thanks to everyone who contributed to this project! Your support is greatly appreciated.

---

**WpCracker** is a powerful tool for WordPress security testing. Use it responsibly and only on systems you have explicit permission to test.

---

[![GitHub stars](https://img.shields.io/github/stars/HackfutSec/WpCracker?style=social)](https://github.com/HackfutSec/WpCracker/stargazers)  
⭐ If you like this project, don't forget to give it a star on GitHub!

---

---

### 📌 Notes
- Ensure you have proper authorization before using this tool.
- This tool is intended for educational purposes and legitimate security testing.

---

**Happy Hacking!** 🚀
