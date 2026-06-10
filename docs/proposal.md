# Đề xuất đề tài

**Môn học:** Hệ hỗ trợ ra quyết định  
**Nhóm:** Nhóm 5  
**Tên đề tài:** Hệ thống hỗ trợ tư vấn pháp lý và khuyến nghị hướng xử lý tình huống Luật Lao động Việt Nam dựa trên RAG đa nguồn

## 1. Bối cảnh và vấn đề

Người lao động, chuyên viên nhân sự và chủ doanh nghiệp nhỏ thường gặp khó khăn khi xử lý các tình huống liên quan đến hợp đồng lao động, tiền lương, chấm dứt hợp đồng, sa thải, bảo hiểm, thai sản hoặc kỷ luật lao động. Thông tin pháp luật tuy có sẵn trên các cổng văn bản pháp luật, nhưng thường dài, khó đọc, nhiều văn bản đã hết hiệu lực và đòi hỏi người tra cứu phải biết đúng thuật ngữ pháp lý.

Trong khi đó, các chatbot sử dụng mô hình ngôn ngữ lớn có thể diễn giải thông tin dễ hiểu hơn, nhưng tồn tại rủi ro nghiêm trọng là sinh ra căn cứ pháp lý không chính xác, trích dẫn sai điều khoản hoặc đưa ra khuyến nghị thiếu kiểm chứng. Với miền pháp lý, những sai lệch này có thể ảnh hưởng trực tiếp đến quyết định của người dùng.

Vì vậy, nhóm đề xuất xây dựng một hệ thống hỗ trợ ra quyết định trong lĩnh vực Luật Lao động, sử dụng mô hình Retrieval-Augmented Generation (RAG) kết hợp dữ liệu pháp luật tĩnh và dữ liệu tình huống thực tế động. Hệ thống không thay thế luật sư, mà đóng vai trò công cụ hỗ trợ người dùng hiểu tình huống, xác định căn cứ pháp lý liên quan và cân nhắc các hướng xử lý phù hợp.

## 2. Mục tiêu hệ thống

Hệ thống hướng tới các mục tiêu chính sau:

1. Truy xuất đúng các quy định pháp luật lao động còn hiệu lực có liên quan đến tình huống người dùng mô tả.
2. Diễn giải căn cứ pháp lý bằng ngôn ngữ dễ hiểu, có trích dẫn rõ điều, khoản và tên văn bản.
3. Bổ sung ví dụ thực tiễn từ báo chí hoặc nguồn tư vấn pháp luật để tăng khả năng kiểm chứng.
4. Đưa ra các phương án xử lý có cấu trúc, ví dụ thương lượng, gửi khiếu nại, liên hệ cơ quan quản lý lao động hoặc khởi kiện.
5. So sánh hiệu quả giữa RAG truyền thống và Agentic RAG đa nguồn theo các tiêu chí phù hợp với hệ hỗ trợ ra quyết định.

## 3. Người dùng mục tiêu

Người dùng chính của hệ thống gồm:

- Người lao động cần hiểu quyền lợi và lựa chọn hành động trong một tranh chấp lao động.
- Chuyên viên nhân sự cần kiểm tra nhanh quy định trước khi xử lý một vụ việc nội bộ.
- Chủ doanh nghiệp nhỏ cần tham khảo hướng xử lý đúng luật trong các tình huống lao động phổ biến.

## 4. Input và Output

### 4.1. Input

Input của hệ thống là câu hỏi hoặc đoạn mô tả tình huống bằng ngôn ngữ tự nhiên. Ví dụ:

> "Công ty nợ lương tôi 2 tháng và yêu cầu tôi ký đơn nghỉ việc. Tôi có thể khiếu nại hoặc kiện được không?"

Hệ thống cần xử lý các câu hỏi không có cấu trúc, có thể thiếu thuật ngữ pháp lý hoặc chứa nhiều vấn đề pháp luật cùng lúc.

### 4.2. Output

Output là một báo cáo tư vấn hỗ trợ ra quyết định, gồm các phần:

1. **Tóm tắt tình huống:** Xác định vấn đề pháp lý chính trong mô tả của người dùng.
2. **Căn cứ pháp lý:** Trích dẫn điều, khoản, tên văn bản và trạng thái hiệu lực của quy định liên quan.
3. **Diễn giải:** Giải thích ngắn gọn quy định bằng ngôn ngữ dễ hiểu.
4. **Kiểm chứng thực tiễn:** Tóm tắt một hoặc một số trường hợp tương tự từ báo chí, trang tư vấn pháp luật hoặc nguồn công khai, kèm URL.
5. **Khuyến nghị hướng xử lý:** Đề xuất các bước người dùng có thể cân nhắc, phân theo mức độ nhẹ đến mạnh như thương lượng, lập hồ sơ chứng cứ, gửi đơn khiếu nại, yêu cầu hòa giải hoặc khởi kiện.
6. **Cảnh báo giới hạn:** Nêu rõ hệ thống chỉ hỗ trợ tham khảo và người dùng nên liên hệ luật sư hoặc cơ quan có thẩm quyền trong trường hợp phức tạp.

## 5. Nguồn dữ liệu

### 5.1. Nguồn 1: Văn bản pháp luật

- **Nguồn dự kiến:** Bộ dữ liệu `th1nhng0/vietnamese-legal-documents`, được crawl từ cơ sở dữ liệu văn bản pháp luật Việt Nam.
- **Dạng dữ liệu:** HTML hoặc raw text của văn bản pháp luật, kèm metadata như loại văn bản, ngày ban hành, lĩnh vực, trạng thái hiệu lực.
- **Quy mô ban đầu:** Khoảng hơn 176.000 văn bản pháp luật trong toàn bộ dataset.
- **Phạm vi sử dụng:** Lọc các văn bản thuộc lĩnh vực lao động và ưu tiên các văn bản còn hiệu lực.
- **Vai trò trong hệ thống:** Cơ sở tri thức chính để truy xuất căn cứ pháp lý chính xác.

### 5.2. Nguồn 2: Báo chí và tình huống thực tế

- **Nguồn dự kiến:** API tìm kiếm như DuckDuckGo hoặc Google Search, ưu tiên các trang báo chính thống, trang tư vấn pháp luật và nguồn có URL kiểm chứng được.
- **Dạng dữ liệu:** Nội dung bài viết được trích xuất tự động, tiêu đề, ngày đăng nếu có và URL.
- **Quy mô sử dụng:** Truy xuất động theo từng câu hỏi, dự kiến 1-3 nguồn cho mỗi truy vấn.
- **Vai trò trong hệ thống:** Bổ sung ví dụ thực tiễn và giúp người dùng hiểu cách quy định có thể được áp dụng trong đời sống.

## 6. Phân tích dữ liệu ban đầu

Từ kết quả EDA trên nhóm văn bản thuộc lĩnh vực lao động, nhóm ghi nhận một số đặc điểm quan trọng:

- Tập dữ liệu sau khi lọc theo lĩnh vực lao động có 483 văn bản.
- Về loại văn bản, Quyết định chiếm khoảng 34.0%, Thông tư chiếm 33.5% và Nghị định chiếm 8.5%.
- Độ dài văn bản có độ lệch lớn. Trung bình một văn bản có khoảng 2.352 từ, trong khi văn bản dài nhất lên tới 62.335 từ.
- Một phần dữ liệu có nội dung rỗng hoặc không đủ chất lượng để đưa trực tiếp vào chỉ mục tìm kiếm.
- Về trạng thái hiệu lực, khoảng 52.0% văn bản đã hết hiệu lực và khoảng 42.4% còn hiệu lực.

Các đặc điểm này cho thấy hệ thống cần có bước tiền xử lý nghiêm túc trước khi đưa dữ liệu vào mô hình truy xuất. Đặc biệt, việc lọc văn bản hết hiệu lực và chia nhỏ văn bản theo cấu trúc pháp lý là yếu tố quan trọng để giảm rủi ro trả lời sai căn cứ.

## 7. Thách thức dữ liệu và hướng xử lý

### 7.1. Văn bản hết hiệu lực

Vì tỷ lệ văn bản hết hiệu lực khá cao, hệ thống sẽ sử dụng metadata để hard-filter các văn bản không còn hiệu lực trước khi lập chỉ mục. Trong trường hợp cần nhắc đến văn bản cũ, hệ thống phải ghi rõ trạng thái hiệu lực thay vì trình bày như căn cứ hiện hành.

### 7.2. Văn bản quá dài và có cấu trúc phức tạp

Nếu chia văn bản theo kích thước cố định, hệ thống có thể làm vỡ cấu trúc pháp lý như Chương, Mục, Điều, Khoản. Nhóm dự kiến dùng BeautifulSoup để bóc tách HTML và chia chunk theo đơn vị ngữ nghĩa pháp lý, ưu tiên Điều và Khoản. Metadata của mỗi chunk sẽ lưu tên văn bản, số hiệu, điều khoản, ngày ban hành và trạng thái hiệu lực.

### 7.3. Rủi ro nhiễu từ dữ liệu web

Nguồn báo chí và internet có thể không đầy đủ hoặc không mang tính pháp lý chính thức. Vì vậy, dữ liệu web chỉ được dùng làm minh họa thực tiễn, không được xem là căn cứ pháp lý chính. Hệ thống cần tách rõ "căn cứ pháp lý" và "ví dụ thực tiễn" trong output.

## 8. Hai giải pháp đề xuất

### 8.1. Giải pháp 1: RAG truyền thống chỉ dùng văn bản pháp luật

Giải pháp đầu tiên sử dụng kiến trúc RAG cơ bản. Câu hỏi của người dùng được chuyển thành embedding, sau đó hệ thống truy xuất các chunk pháp luật liên quan trong vector database. LLM sử dụng các đoạn truy xuất được để tổng hợp câu trả lời.

Luồng xử lý:

1. Người dùng nhập câu hỏi.
2. Hệ thống chuẩn hóa câu hỏi và tạo embedding.
3. Vector database trả về các điều luật liên quan nhất.
4. LLM tạo câu trả lời dựa trên các đoạn luật được truy xuất.

Ưu điểm của hướng này là đơn giản, tốc độ nhanh và dễ đánh giá. Hạn chế là câu trả lời có thể thiếu ví dụ thực tế, chưa hỗ trợ tốt việc so sánh các lựa chọn hành động và ít tạo cảm giác "hỗ trợ ra quyết định" cho người dùng.

### 8.2. Giải pháp 2: Agentic RAG đa nguồn

Giải pháp thứ hai xây dựng một Agent có khả năng điều phối nhiều công cụ. Agent trước hết truy xuất căn cứ pháp lý từ vector database. Sau đó, nếu cần minh họa thực tế, Agent sinh truy vấn tìm kiếm, gọi công cụ web search, đọc các nguồn phù hợp và tổng hợp thành báo cáo tư vấn.

Luồng xử lý:

1. Người dùng nhập câu hỏi.
2. Agent phân tích tình huống và xác định vấn đề pháp lý chính.
3. Agent gọi công cụ truy xuất luật để lấy căn cứ pháp lý.
4. Agent tạo truy vấn tìm kiếm các tình huống thực tế tương tự.
5. Agent tổng hợp luật, ví dụ thực tế và khuyến nghị.
6. Hệ thống trả về báo cáo có cấu trúc cho giao diện.

Ưu điểm của hướng này là output giàu ngữ cảnh hơn, có nguồn kiểm chứng và phù hợp hơn với mục tiêu hỗ trợ quyết định. Hạn chế là thời gian phản hồi dài hơn, phụ thuộc chất lượng kết quả tìm kiếm web và cần kiểm soát chặt chẽ để tránh Agent sử dụng nguồn không đáng tin cậy.

## 9. Tiêu chí đánh giá

Nhóm dự kiến so sánh hai giải pháp theo các tiêu chí sau:

| Nhóm tiêu chí | Chỉ số | Mục đích |
| --- | --- | --- |
| Truy xuất | Hit Rate, MRR | Đo hệ thống có tìm đúng điều luật liên quan hay không |
| Chất lượng câu trả lời | Faithfulness, Answer Relevance | Đo câu trả lời có bám sát nguồn và đúng trọng tâm câu hỏi hay không |
| Minh bạch | Citation quality, URL availability | Đánh giá khả năng người dùng tự kiểm chứng căn cứ |
| Hiệu quả sử dụng | Latency | So sánh thời gian phản hồi giữa RAG truyền thống và Agentic RAG |
| Giá trị hỗ trợ quyết định | User Utility rubric | Đánh giá câu trả lời có đưa ra lựa chọn hành động rõ ràng và hữu ích hay không |

Với phần đánh giá tự động, nhóm dự kiến sử dụng RAGAS cho các chỉ số như Faithfulness và Answer Relevance. Với phần đánh giá truy xuất, nhóm sẽ xây dựng bộ câu hỏi ground truth gồm 30-50 tình huống lao động phổ biến, mỗi câu hỏi gắn với điều luật hoặc nhóm điều luật kỳ vọng.

## 10. Kết quả kỳ vọng

Kết quả cuối cùng của dự án gồm:

- Một pipeline xử lý dữ liệu pháp luật lao động, lọc văn bản còn hiệu lực và chia chunk theo cấu trúc pháp lý.
- Một hệ thống RAG truyền thống làm baseline.
- Một hệ thống Agentic RAG đa nguồn có khả năng kết hợp căn cứ pháp luật và tình huống thực tế.
- Một giao diện Streamlit cho phép người dùng nhập tình huống và xem báo cáo tư vấn.
- Một bộ đánh giá gồm câu hỏi ground truth, chỉ số định lượng và nhận xét định tính.
- Báo cáo so sánh ưu nhược điểm của hai giải pháp theo góc nhìn hệ hỗ trợ ra quyết định.

## 11. Giới hạn phạm vi

Dự án tập trung vào mục tiêu học thuật và minh họa kỹ thuật DSS, không cung cấp dịch vụ tư vấn pháp lý chính thức. Trong phạm vi môn học, nhóm chỉ tập trung vào một số nhóm tình huống phổ biến của Luật Lao động như nợ lương, chấm dứt hợp đồng, sa thải, thử việc, thai sản và bảo hiểm xã hội. Các tình huống phức tạp, có yếu tố tố tụng hoặc cần phân tích hồ sơ chi tiết sẽ được hệ thống khuyến nghị liên hệ luật sư hoặc cơ quan có thẩm quyền.

## 12. Nhận xét tổng quan

Đề tài có tính phù hợp cao với môn Hệ hỗ trợ ra quyết định vì không chỉ dừng ở việc hỏi đáp văn bản, mà còn hướng đến hỗ trợ người dùng lựa chọn hành động trong một tình huống có rủi ro. Điểm mạnh của đề tài là có nguồn dữ liệu rõ ràng, có baseline để so sánh, có tiêu chí đánh giá định lượng và có khả năng demo trực quan.

Điểm cần kiểm soát là phạm vi. Nếu nhóm cố xử lý toàn bộ pháp luật lao động và mọi dạng tranh chấp, hệ thống sẽ dễ bị loãng và khó đánh giá. Nhóm nên chọn một tập tình huống trọng tâm, xây dựng ground truth tốt và chứng minh rằng giải pháp Agentic RAG tạo ra khuyến nghị minh bạch, có căn cứ hơn baseline RAG truyền thống.
