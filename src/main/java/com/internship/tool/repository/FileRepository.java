package com.internship.tool.repository;

import com.internship.tool.entity.FileData;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FileRepository extends JpaRepository<FileData, Long> {
}
